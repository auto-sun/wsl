from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect, render

from apps.common.auth import SESSION_USER_KEY, is_demo_authenticated


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        if (
            username == settings.DEMO_ACCOUNT["username"]
            and password == settings.DEMO_ACCOUNT["password"]
        ):
            request.session[SESSION_USER_KEY] = {
                "username": settings.DEMO_ACCOUNT["username"],
                "display_name": settings.DEMO_ACCOUNT["display_name"],
                "role": settings.DEMO_ACCOUNT["role"],
            }
            request.session.cycle_key()
            return redirect("/dashboard")
        messages.error(request, "账号或密码错误，请使用演示账号登录。")

    if is_demo_authenticated(request):
        return redirect("/dashboard")

    return render(
        request,
        "login.html",
        {
            "page_title": "登录",
            "page_key": "login",
            "demo_account": {
                "username": settings.DEMO_ACCOUNT["username"],
                "password": settings.DEMO_ACCOUNT["password"],
            },
            "system_meta": settings.SYSTEM_META,
        },
    )


def logout_view(request):
    request.session.flush()
    return redirect("/login")
