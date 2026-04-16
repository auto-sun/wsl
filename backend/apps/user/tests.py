from django.conf import settings
from django.test import Client, TestCase


class DemoLoginTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_with_demo_account_redirects_to_dashboard(self):
        response = self.client.post(
            "/login",
            {
                "username": settings.DEMO_ACCOUNT["username"],
                "password": settings.DEMO_ACCOUNT["password"],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/dashboard")

    def test_login_with_invalid_credentials_stays_on_login_page(self):
        response = self.client.post(
            "/login",
            {
                "username": "wrong",
                "password": "wrong",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "账号或密码错误")

    def test_logout_clears_session(self):
        self.client.post(
            "/login",
            {
                "username": settings.DEMO_ACCOUNT["username"],
                "password": settings.DEMO_ACCOUNT["password"],
            },
        )
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/login")

        protected_response = self.client.get("/dashboard")
        self.assertEqual(protected_response.status_code, 302)
        self.assertEqual(protected_response.headers["Location"], "/login")
