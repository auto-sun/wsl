from django.conf import settings

from .auth import get_demo_user


NAV_ITEMS = [
    {"label": "系统首页", "path": "/dashboard", "key": "dashboard"},
    {"label": "长势监测", "path": "/monitoring", "key": "monitoring"},
    {"label": "病虫害检测", "path": "/diagnosis", "key": "diagnosis"},
    {"label": "处方图策略", "path": "/decision", "key": "decision"},
    {"label": "设备管理", "path": "/devices", "key": "devices"},
    {"label": "API 文档", "path": "/api-docs", "key": "api-docs"},
]


def build_breadcrumbs(path):
    current = next((item for item in NAV_ITEMS if item["path"] == path), None)
    if path == "/login":
        return [{"label": "登录", "path": "/login"}]
    if current is None:
        return [
            {"label": "系统首页", "path": "/dashboard"},
            {"label": "页面不存在", "path": path},
        ]
    if path == "/dashboard":
        return [{"label": "系统首页", "path": "/dashboard"}]
    return [
        {"label": "系统首页", "path": "/dashboard"},
        {"label": current["label"], "path": current["path"]},
    ]


def layout_context(request):
    return {
        "system_meta": settings.SYSTEM_META,
        "nav_items": NAV_ITEMS,
        "current_path": request.path,
        "current_user": get_demo_user(request),
        "breadcrumbs": build_breadcrumbs(request.path),
    }
