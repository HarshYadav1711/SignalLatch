import json
from dataclasses import dataclass
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from content.models import ContentItem
from flags.models import Flag
from keywords.models import Keyword


@dataclass
class ScanResult:
    created: int = 0
    updated: int = 0
    suppressed: int = 0
    scanned_pairs: int = 0


def _compute_score(keyword_name: str, title: str, body: str):
    keyword = (keyword_name or "").strip().lower()
    title_text = (title or "").lower()
    body_text = (body or "").lower()

    if not keyword:
        return None
    if title_text == keyword:
        return Decimal("100.00")
    if keyword in title_text:
        return Decimal("70.00")
    if keyword in body_text:
        return Decimal("40.00")
    return None


def _load_content_from_dataset_if_needed():
    if ContentItem.objects.exists():
        return

    dataset_path = settings.CONTENT_DATASET_PATH
    if not dataset_path.exists():
        return

    with dataset_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    for row in payload:
        source = (row.get("source") or "mock_dataset").strip()
        title = (row.get("title") or "").strip()
        body = row.get("body") or ""
        parsed = parse_datetime(row.get("last_updated") or "")
        last_updated = parsed if parsed else timezone.now()
        if not title:
            continue
        ContentItem.objects.update_or_create(
            source=source,
            title=title,
            defaults={"body": body, "last_updated": last_updated},
        )


@transaction.atomic
def run_scan():
    _load_content_from_dataset_if_needed()

    result = ScanResult()
    keywords = list(Keyword.objects.all())
    content_items = list(ContentItem.objects.all())

    for keyword in keywords:
        for content_item in content_items:
            result.scanned_pairs += 1
            score = _compute_score(keyword.name, content_item.title, content_item.body)
            if score is None:
                continue

            flag, created = Flag.objects.get_or_create(
                keyword=keyword,
                content_item=content_item,
                defaults={"score": score},
            )

            if created:
                result.created += 1
                continue

            # Suppress previously irrelevant flags until content changes.
            if (
                flag.status == Flag.Status.IRRELEVANT
                and flag.reviewed_content_last_updated == content_item.last_updated
            ):
                result.suppressed += 1
                continue

            flag.score = score
            if flag.status == Flag.Status.IRRELEVANT:
                flag.status = Flag.Status.PENDING
                flag.reviewed_at = None
                flag.reviewed_content_last_updated = None
            flag.save(
                update_fields=[
                    "score",
                    "status",
                    "reviewed_at",
                    "reviewed_content_last_updated",
                ]
            )
            result.updated += 1

    return result
