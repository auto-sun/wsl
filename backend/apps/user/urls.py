from django.urls import path

from .views import (
    admin_login_view,
    admin_register_view,
    legacy_login_view,
    legacy_register_view,
    logout_view,
    user_login_view,
    user_register_view,
)


urlpatterns = [
    path("login", legacy_login_view, name="login"),
    path("register", legacy_register_view, name="register"),
    path("user/login", user_login_view, name="user-login"),
    path("user/register", user_register_view, name="user-register"),
    path("admin/login", admin_login_view, name="admin-login"),
    path("admin/register", admin_register_view, name="admin-register"),
    path("logout", logout_view, name="logout"),
]
