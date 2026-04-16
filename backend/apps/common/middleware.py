from django.shortcuts import redirect

from .auth import is_demo_authenticated


class DemoLoginRequiredMiddleware:
    """
    基础登录校验占位。

    当前阶段：
    - 仅保护 HTML 页面访问
    - API 暂保持可直接访问，便于开发演示和调试

    后续阶段：
    - 可切换为更细粒度权限控制
    - 可对接 Django Auth / JWT / 单点登录
    """

    protected_paths = {
        "/dashboard",
        "/monitoring",
        "/diagnosis",
        "/decision",
        "/devices",
        "/api-docs",
    }

    allowed_prefixes = ("/login", "/logout", "/api/", "/static/", "/media/", "/admin/")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if path.startswith(self.allowed_prefixes):
            return self.get_response(request)

        if path in self.protected_paths and not is_demo_authenticated(request):
            return redirect("/login")

        return self.get_response(request)
