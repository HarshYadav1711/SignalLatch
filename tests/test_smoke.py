import json

from django.test import TestCase


class RoutingSmokeTests(TestCase):
    def test_root_endpoint_exists(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_keywords_create_endpoint_exists(self):
        response = self.client.post(
            "/keywords/",
            data=json.dumps({"name": "django"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
