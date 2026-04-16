from django.test import Client, TestCase


class PlatformSmokeTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_page_is_available(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_api_and_dashboard_api(self):
        response = self.client.post(
            "/api/auth/login/",
            data={"username": "admin", "password": "123456"},
        )
        self.assertEqual(response.status_code, 200)
        overview = self.client.get("/api/dashboard/overview/")
        self.assertEqual(overview.status_code, 200)
        self.assertEqual(overview.json()["code"], 0)

    def test_protected_page_redirects_without_login(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 302)

    def test_all_core_pages_load_after_login(self):
        self.client.post(
            "/api/auth/login/",
            data={"username": "admin", "password": "123456"},
        )
        for path in [
            "/dashboard/",
            "/growth/",
            "/disease-detection/",
            "/prescription/",
            "/devices/",
            "/api-docs/",
        ]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200, msg=path)
