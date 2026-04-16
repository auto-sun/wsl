from django.conf import settings
from django.test import Client, TestCase


class SkeletonSmokeTests(TestCase):
    def setUp(self):
        self.client = Client()

    def login_demo_user(self):
        return self.client.post(
            "/login",
            {
                "username": settings.DEMO_ACCOUNT["username"],
                "password": settings.DEMO_ACCOUNT["password"],
            },
        )

    def test_login_page_is_available(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)

    def test_protected_pages_redirect_when_not_logged_in(self):
        for path in ["/dashboard", "/monitoring", "/diagnosis", "/decision", "/devices", "/api-docs"]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 302, msg=path)
            self.assertEqual(response.headers["Location"], "/login")

    def test_protected_pages_are_available_after_login(self):
        login_response = self.login_demo_user()
        self.assertEqual(login_response.status_code, 302)
        self.assertEqual(login_response.headers["Location"], "/dashboard")

        for path in ["/dashboard", "/monitoring", "/diagnosis", "/decision", "/devices", "/api-docs"]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, msg=path)

    def test_api_endpoints_are_available(self):
        for path in ["/api/", "/api/health", "/api/dashboard/overview"]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, msg=path)
            self.assertEqual(response.json()["code"], 0)

    def test_unknown_page_returns_custom_404(self):
        response = self.client.get("/unknown-page-demo")
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "页面不存在", status_code=404)
