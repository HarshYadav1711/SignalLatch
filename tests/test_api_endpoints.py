import json
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from content.models import ContentItem
from flags.models import Flag
from keywords.models import Keyword


class ApiEndpointTests(TestCase):
    def test_post_keywords_creates_keyword(self):
        response = self.client.post(
            "/keywords/",
            data=json.dumps({"name": "  Django  "}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["keyword"]["name"], "django")

    def test_post_scan_triggers_scan(self):
        Keyword.objects.create(name="django")
        ContentItem.objects.create(
            source="test",
            title="Django Assignment",
            body="body",
            last_updated=timezone.now(),
        )

        response = self.client.post("/scan/", data="{}", content_type="application/json")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["message"], "Scan completed.")
        self.assertIn("scan", payload)
        self.assertIn("created", payload["scan"])
        self.assertIn("updated", payload["scan"])
        self.assertIn("suppressed", payload["scan"])
        self.assertIn("scanned_pairs", payload["scan"])

    def test_get_flags_supports_filters(self):
        keyword = Keyword.objects.create(name="django")
        item = ContentItem.objects.create(
            source="test",
            title="Django Assignment",
            body="body",
            last_updated=timezone.now(),
        )
        Flag.objects.create(
            keyword=keyword,
            content_item=item,
            score="70.00",
            status=Flag.Status.PENDING,
        )

        response = self.client.get("/flags/?status=pending&min_score=50.00&keyword=djan")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["status"], "pending")
        self.assertEqual(payload["results"][0]["keyword_name"], "django")

    def test_patch_flags_updates_irrelevant_review_snapshot(self):
        keyword = Keyword.objects.create(name="django")
        item = ContentItem.objects.create(
            source="test",
            title="Django Assignment",
            body="body",
            last_updated=timezone.now(),
        )
        flag = Flag.objects.create(keyword=keyword, content_item=item, score="70.00")

        response = self.client.patch(
            f"/flags/{flag.id}/",
            data=json.dumps({"status": "irrelevant"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        flag.refresh_from_db()
        self.assertEqual(flag.status, Flag.Status.IRRELEVANT)
        self.assertEqual(flag.reviewed_content_last_updated, item.last_updated)

    def test_full_assignment_flow_end_to_end(self):
        created = self.client.post(
            "/keywords/",
            data=json.dumps({"name": "Django"}),
            content_type="application/json",
        )
        self.assertEqual(created.status_code, 201)

        content_item = ContentItem.objects.create(
            source="test",
            title="Django SignalLatch",
            body="Local assignment content.",
            last_updated=timezone.now(),
        )

        first_scan = self.client.post("/scan/", data="{}", content_type="application/json")
        self.assertEqual(first_scan.status_code, 200)
        self.assertEqual(first_scan.json()["scan"]["created"], 1)

        listed = self.client.get("/flags/?status=pending")
        self.assertEqual(listed.status_code, 200)
        self.assertEqual(listed.json()["count"], 1)
        flag_payload = listed.json()["results"][0]
        self.assertEqual(flag_payload["score"], "70.00")
        flag_id = flag_payload["id"]

        reviewed = self.client.patch(
            f"/flags/{flag_id}/",
            data=json.dumps({"status": "irrelevant"}),
            content_type="application/json",
        )
        self.assertEqual(reviewed.status_code, 200)
        self.assertEqual(reviewed.json()["flag"]["status"], "irrelevant")
        self.assertIsNotNone(reviewed.json()["flag"]["reviewed_content_last_updated"])

        suppressed_scan = self.client.post("/scan/", data="{}", content_type="application/json")
        self.assertEqual(suppressed_scan.status_code, 200)
        self.assertEqual(suppressed_scan.json()["scan"]["suppressed"], 1)

        content_item.last_updated = content_item.last_updated + timedelta(minutes=1)
        content_item.save(update_fields=["last_updated"])

        resurfaced_scan = self.client.post("/scan/", data="{}", content_type="application/json")
        self.assertEqual(resurfaced_scan.status_code, 200)
        self.assertEqual(resurfaced_scan.json()["scan"]["updated"], 1)

        latest = self.client.get(f"/flags/?keyword=django&min_score=70.00")
        self.assertEqual(latest.status_code, 200)
        self.assertEqual(latest.json()["count"], 1)
        self.assertEqual(latest.json()["results"][0]["status"], "pending")
