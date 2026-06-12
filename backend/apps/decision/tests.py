from django.contrib.auth.models import User
from django.test import Client, TestCase


class DecisionSmokeTests(TestCase):
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

    def test_decision_page_is_available(self):
        response = self.client.get("/decision")
        self.assertEqual(response.status_code, 200)

    def test_decision_api_endpoints_are_available(self):
        plans = self.client.get("/api/decision/plans")
        self.assertEqual(plans.status_code, 200)
        self.assertEqual(plans.json()["code"], 0)

        generated = self.client.post(
            "/api/decision/generate",
            data='{"block_code":"B02"}',
            content_type="application/json",
        )
        self.assertEqual(generated.status_code, 200)
        self.assertEqual(generated.json()["code"], 0)

        plan_code = generated.json()["data"]["generated_plan"]["plan_code"]
        dispatched = self.client.post(
            "/api/decision/dispatch",
            data=f'{{"plan_code":"{plan_code}"}}',
            content_type="application/json",
        )
        self.assertEqual(dispatched.status_code, 200)
        self.assertEqual(dispatched.json()["code"], 0)
