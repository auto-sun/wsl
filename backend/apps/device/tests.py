import json

from django.conf import settings
from django.test import Client, TestCase


class DeviceSmokeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post(
            "/login",
            {
                "username": settings.DEMO_ACCOUNT["username"],
                "password": settings.DEMO_ACCOUNT["password"],
            },
        )

    def test_devices_page_is_available(self):
        response = self.client.get("/devices")
        self.assertEqual(response.status_code, 200)

    def test_device_api_endpoints_are_available(self):
        for path in ["/api/devices/status", "/api/devices/list", "/api/devices/logs?device_code=CAM-01"]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, msg=path)
            self.assertEqual(response.json()["code"], 0)

    def test_device_actions_return_placeholder(self):
        tested = self.client.post(
            "/api/devices/test",
            data=json.dumps({"device_code": "CAM-01"}),
            content_type="application/json",
        )
        self.assertEqual(tested.status_code, 200)
        self.assertEqual(tested.json()["code"], 0)

        commanded = self.client.post(
            "/api/devices/command",
            data=json.dumps({"device_code": "CTRL-01", "command": "open_valve"}),
            content_type="application/json",
        )
        self.assertEqual(commanded.status_code, 200)
        self.assertEqual(commanded.json()["code"], 0)
