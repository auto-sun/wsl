from django.urls import include, path

from .views import api_docs_view, dashboard_view, index_view


urlpatterns = [
    path("", index_view, name="index"),
    path("dashboard", dashboard_view, name="dashboard"),
    path("api-docs", api_docs_view, name="api-docs"),
    path("api/", include("apps.common.api_urls")),
]
