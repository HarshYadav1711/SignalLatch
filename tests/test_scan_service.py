from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from content.models import ContentItem
from flags.models import Flag
from keywords.models import Keyword
from services.flag_review_service import mark_flag_irrelevant
from services.scan_service import run_scan


class ScanServiceTests(TestCase):
    def test_exact_title_match_scores_100(self):
        Keyword.objects.create(name="django")
        item = ContentItem.objects.create(
            source="test",
            title="django",
            body="body text",
            last_updated=timezone.now(),
        )

        run_scan()

        flag = Flag.objects.get(content_item=item)
        self.assertEqual(flag.score, Decimal("100.00"))

    def test_partial_title_match_scores_70(self):
        Keyword.objects.create(name="django")
        item = ContentItem.objects.create(
            source="test",
            title="Django Project Kickoff",
            body="body text",
            last_updated=timezone.now(),
        )

        run_scan()

        flag = Flag.objects.get(content_item=item)
        self.assertEqual(flag.score, Decimal("70.00"))

    def test_body_only_match_scores_40(self):
        Keyword.objects.create(name="sqlite")
        item = ContentItem.objects.create(
            source="test",
            title="Backend Assignment",
            body="This item references SQLITE in body only.",
            last_updated=timezone.now(),
        )

        run_scan()

        flag = Flag.objects.get(content_item=item)
        self.assertEqual(flag.score, Decimal("40.00"))

    def test_irrelevant_flag_is_suppressed_when_content_unchanged(self):
        keyword = Keyword.objects.create(name="django")
        item = ContentItem.objects.create(
            source="test",
            title="Django Project Kickoff",
            body="body text",
            last_updated=timezone.now(),
        )
        flag = Flag.objects.create(keyword=keyword, content_item=item, score=Decimal("70.00"))
        mark_flag_irrelevant(flag)

        result = run_scan()
        flag.refresh_from_db()

        self.assertEqual(result.suppressed, 1)
        self.assertEqual(flag.status, Flag.Status.IRRELEVANT)
        self.assertEqual(flag.reviewed_content_last_updated, item.last_updated)

    def test_irrelevant_flag_reappears_after_content_change(self):
        keyword = Keyword.objects.create(name="django")
        original_updated = timezone.now()
        item = ContentItem.objects.create(
            source="test",
            title="Django Project Kickoff",
            body="body text",
            last_updated=original_updated,
        )
        flag = Flag.objects.create(keyword=keyword, content_item=item, score=Decimal("70.00"))
        mark_flag_irrelevant(flag)

        item.last_updated = original_updated + timedelta(minutes=1)
        item.save(update_fields=["last_updated"])

        result = run_scan()
        flag.refresh_from_db()

        self.assertEqual(result.suppressed, 0)
        self.assertEqual(result.updated, 1)
        self.assertEqual(flag.status, Flag.Status.PENDING)
        self.assertIsNone(flag.reviewed_content_last_updated)
