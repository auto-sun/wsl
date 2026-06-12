from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings


class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="normal_user",
            password="123456",
            first_name="普通用户",
        )
        self.admin = User.objects.create_user(
            username="admin_user",
            password="123456",
            first_name="管理员",
            is_staff=True,
        )

    def test_user_login_page_is_available(self):
        response = self.client.get("/user/login")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "普通用户登录")

    def test_admin_login_page_is_available(self):
        response = self.client.get("/admin/login")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "管理员登录")

    def test_user_login_with_valid_account_redirects_to_dashboard(self):
        response = self.client.post(
            "/user/login",
            {"username": "normal_user", "password": "123456"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/dashboard")

    def test_admin_login_with_valid_account_redirects_to_dashboard(self):
        response = self.client.post(
            "/admin/login",
            {"username": "admin_user", "password": "123456"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/dashboard")

    def test_user_cannot_login_through_admin_entry(self):
        response = self.client.post(
            "/admin/login",
            {"username": "normal_user", "password": "123456"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "该账号不是管理员账号")

    def test_admin_cannot_login_through_user_entry(self):
        response = self.client.post(
            "/user/login",
            {"username": "admin_user", "password": "123456"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "该账号是管理员账号")

    def test_login_with_invalid_credentials_stays_on_login_page(self):
        response = self.client.post(
            "/user/login",
            {"username": "wrong", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "账号或密码错误")

    def test_user_register_creates_normal_user(self):
        response = self.client.post(
            "/user/register",
            {
                "username": "new_user",
                "email": "new@example.com",
                "password": "123456",
                "password_confirm": "123456",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/user/login")
        user = User.objects.get(username="new_user")
        self.assertFalse(user.is_staff)
        self.assertEqual(user.first_name, "new_user")

    @override_settings(ADMIN_INVITE_CODE="liyang")
    def test_admin_register_requires_invite_code(self):
        response = self.client.post(
            "/admin/register",
            {
                "username": "bad_admin",
                "password": "123456",
                "password_confirm": "123456",
                "invite_code": "wrong",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "管理员邀请码错误")
        self.assertFalse(User.objects.filter(username="bad_admin").exists())

    @override_settings(ADMIN_INVITE_CODE="liyang")
    def test_admin_register_creates_admin_user(self):
        response = self.client.post(
            "/admin/register",
            {
                "username": "new_admin",
                "email": "admin@example.com",
                "password": "123456",
                "password_confirm": "123456",
                "invite_code": "liyang",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/admin/login")
        user = User.objects.get(username="new_admin")
        self.assertTrue(user.is_staff)
        self.assertEqual(user.first_name, "new_admin")

    def test_logout_clears_session(self):
        self.client.login(username="normal_user", password="123456")
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.headers["Location"], "/user/login")

        protected_response = self.client.get("/dashboard")
        self.assertEqual(protected_response.status_code, 302)
        self.assertEqual(protected_response.headers["Location"], "/user/login")
