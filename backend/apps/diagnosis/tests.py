from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import Client, TestCase


class DiagnosisSmokeTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.client.post(
            "/login",
            {
                "username": settings.DEMO_ACCOUNT["username"],
                "password": settings.DEMO_ACCOUNT["password"],
            },
        )

    def test_diagnosis_page_is_available(self):
        response = self.client.get("/diagnosis")
        self.assertEqual(response.status_code, 200)

    def test_history_api_is_available(self):
        response = self.client.get("/api/diagnosis/history")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["code"], 0)

    def test_upload_api_returns_mock_result(self):
        upload = SimpleUploadedFile("dragonfruit-test.jpg", b"fake-image-bytes", content_type="image/jpeg")
        response = self.client.post("/api/diagnosis/upload", {"image": upload})
        self.assertEqual(response.status_code, 200)
        payload = response.json()["data"]
        self.assertEqual(payload["status"], "success")
        self.assertIn("/media/diagnosis/", payload["image_url"])
        self.assertIn("result", payload)
        self.assertIn("disease_name", payload["result"])
        self.assertIn("confidence", payload["result"])
        self.assertIn("risk_level", payload["result"])
        self.assertIn("suggestion", payload["result"])
        self.assertIn("boxes", payload["result"])
        self.assertIn("width", payload["result"]["boxes"][0])
        self.assertIn("height", payload["result"]["boxes"][0])
        self.assertIn("score", payload["result"]["boxes"][0])
        self.assertIsInstance(payload["task_id"], int)
