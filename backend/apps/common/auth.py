SESSION_USER_KEY = "demo_user"


def get_demo_user(request):
    return request.session.get(SESSION_USER_KEY)


def is_demo_authenticated(request):
    return bool(get_demo_user(request))
