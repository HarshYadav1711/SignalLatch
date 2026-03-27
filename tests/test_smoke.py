from django.test import TestCase
from django.urls import reverse


class RoutingSmokeTests(TestCase):
    def test_keywords_health_endpoint(self):
        response = self.client.get(reverse('keywords:health'))
        self.assertEqual(response.status_code, 200)
