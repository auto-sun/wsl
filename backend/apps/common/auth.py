SESSION_USER_KEY = "app_user"


def get_current_user(request):
    user = getattr(request, "user", None)
    if not user or not user.is_authenticated:
        return None
    display_name = user.get_full_name() or user.first_name or user.username
    return {
        "username": user.username,
        "display_name": display_name,
        "role": "管理员" if user.is_staff else "普通用户",
    }


def get_demo_user(request):
    return get_current_user(request)


def is_demo_authenticated(request):
    user = getattr(request, "user", None)
    return bool(user and user.is_authenticated)
