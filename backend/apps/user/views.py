from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


ROLE_USER = "user"
ROLE_ADMIN = "admin"


def legacy_login_view(request):
    return user_login_view(request)


def legacy_register_view(request):
    return user_register_view(request)


def user_login_view(request):
    return _login_view(
        request,
        role=ROLE_USER,
        template_name="user_login.html",
        success_message="普通用户登录成功。",
    )


def admin_login_view(request):
    return _login_view(
        request,
        role=ROLE_ADMIN,
        template_name="admin_login.html",
        success_message="管理员登录成功。",
    )


def user_register_view(request):
    return _register_view(
        request,
        role=ROLE_USER,
        template_name="user_register.html",
        success_redirect="/user/login",
        success_message="普通用户注册成功，请登录。",
    )


def admin_register_view(request):
    return _register_view(
        request,
        role=ROLE_ADMIN,
        template_name="admin_register.html",
        success_redirect="/admin/login",
        success_message="管理员注册成功，请登录。",
    )


def logout_view(request):
    auth_logout(request)
    messages.success(request, "已退出登录。")
    return redirect("/user/login")


def _login_view(request, role, template_name, success_message):
    if request.user.is_authenticated:
        return redirect("/dashboard")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)
        if user is None:
            messages.error(request, "账号或密码错误，请重新输入。")
        elif role == ROLE_ADMIN and not user.is_staff:
            messages.error(request, "该账号不是管理员账号，请使用管理员账号登录。")
        elif role == ROLE_USER and user.is_staff:
            messages.error(request, "该账号是管理员账号，请使用管理员登录入口。")
        else:
            auth_login(request, user)
            messages.success(request, success_message)
            return redirect("/dashboard")

    return render(request, template_name, _auth_context(role=role, mode="login"))


def _register_view(request, role, template_name, success_redirect, success_message):
    if request.user.is_authenticated:
        return redirect("/dashboard")

    form_data = {
        "username": "",
        "email": "",
    }
    if request.method == "POST":
        form_data = {
            "username": request.POST.get("username", "").strip(),
            "email": request.POST.get("email", "").strip(),
        }
        password = request.POST.get("password", "")
        password_confirm = request.POST.get("password_confirm", "")
        invite_code = request.POST.get("invite_code", "").strip()

        error_message = _validate_register_payload(
            role=role,
            username=form_data["username"],
            password=password,
            password_confirm=password_confirm,
            invite_code=invite_code,
        )
        if error_message:
            messages.error(request, error_message)
        else:
            user = User.objects.create_user(
                username=form_data["username"],
                email=form_data["email"],
                password=password,
            )
            user.first_name = form_data["username"]
            if role == ROLE_ADMIN:
                user.is_staff = True
            user.save(update_fields=["first_name", "is_staff", "email"])
            messages.success(request, success_message)
            return redirect(success_redirect)

    context = _auth_context(role=role, mode="register")
    context["form_data"] = form_data
    context["invite_required"] = role == ROLE_ADMIN
    return render(request, template_name, context)


def _validate_register_payload(role, username, password, password_confirm, invite_code):
    if not username:
        return "请输入账号。"
    if User.objects.filter(username=username).exists():
        return "账号已存在，请更换账号。"
    if not password:
        return "请输入密码。"
    if len(password) < 6:
        return "密码长度不能少于 6 位。"
    if password != password_confirm:
        return "两次输入的密码不一致。"
    if role == ROLE_ADMIN and invite_code != settings.ADMIN_INVITE_CODE:
        return "管理员邀请码错误。"
    return ""


def _auth_context(role, mode):
    is_admin = role == ROLE_ADMIN
    role_label = "管理员" if is_admin else "普通用户"
    mode_label = "登录" if mode == "login" else "注册"
    return {
        "page_title": f"{role_label}{mode_label}",
        "page_key": f"{role}-{mode}",
        "system_meta": settings.SYSTEM_META,
        "role_label": role_label,
        "is_admin": is_admin,
        "login_url": "/admin/login" if is_admin else "/user/login",
        "register_url": "/admin/register" if is_admin else "/user/register",
        "switch_login_url": "/user/login" if is_admin else "/admin/login",
        "switch_login_label": "普通用户登录" if is_admin else "管理员登录",
        "switch_register_url": "/user/register" if is_admin else "/admin/register",
        "switch_register_label": "普通用户注册" if is_admin else "管理员注册",
    }
