from django.shortcuts import redirect

from .auth import is_demo_authenticated


class DemoLoginRequiredMiddleware:
    """
    页面登录保护。

    当前仅保护 HTML 页面访问，API 暂保持可直接访问，便于开发演示和调试。
    """

    protected_paths = {
        "/dashboard",
        "/monitoring",
        "/diagnosis",
        "/decision",
        "/devices",
        "/api-docs",
    }

    allowed_prefixes = (
        "/login",
        "/register",
        "/user/login",
        "/user/register",
        "/admin/login",
        "/admin/register",
        "/logout",
        "/api/",
        "/static/",
        "/media/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith(self.allowed_prefixes):
            return self.get_response(request)

        if path in self.protected_paths and not is_demo_authenticated(request):
            return redirect("/user/login")

        return self.get_response(request)
