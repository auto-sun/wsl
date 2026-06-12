from django.contrib.auth.models import User
from django.test import Client, TestCase


class MonitoringSmokeTests(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user(
            username="test_user",
            password="123456",
        )
        self.client.post(
            "/login",
            {
                "username": "test_user",
                "password": "123456",
            },
        )

    def test_monitoring_page_is_available(self):
        response = self.client.get("/monitoring")
        self.assertEqual(response.status_code, 200)

    def test_monitoring_api_endpoints_are_available(self):
        for path in ["/api/monitoring/growth-summary", "/api/monitoring/heatmap-data"]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, msg=path)
            self.assertEqual(response.json()["code"], 0)
