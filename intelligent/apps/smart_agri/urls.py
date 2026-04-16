from django.urls import path

from . import api_views, views


urlpatterns = [
    path("", views.RootRedirectView.as_view(), name="root"),
    path("login/", views.LoginPageView.as_view(), name="login"),
    path("dashboard/", views.DashboardPageView.as_view(), name="dashboard"),
    path("growth/", views.GrowthMonitorPageView.as_view(), name="growth-monitor"),
    path(
        "disease-detection/",
        views.DiseaseDetectionPageView.as_view(),
        name="disease-detection",
    ),
    path("prescription/", views.PrescriptionPageView.as_view(), name="prescription"),
    path("devices/", views.DeviceManagementPageView.as_view(), name="device-management"),
    path("api-docs/", views.ApiDocsPageView.as_view(), name="api-docs"),
    path("api/auth/login/", api_views.LoginApiView.as_view(), name="api-login"),
    path("api/auth/logout/", api_views.LogoutApiView.as_view(), name="api-logout"),
    path(
        "api/dashboard/overview/",
        api_views.DashboardOverviewApiView.as_view(),
        name="api-dashboard-overview",
    ),
    path(
        "api/monitoring/growth/",
        api_views.GrowthSummaryApiView.as_view(),
        name="api-growth-summary",
    ),
    path(
        "api/monitoring/heatmap/",
        api_views.GrowthHeatmapApiView.as_view(),
        name="api-growth-heatmap",
    ),
    path(
        "api/disease-detections/",
        api_views.DiseaseDetectionApiView.as_view(),
        name="api-disease-detections",
    ),
    path(
        "api/prescriptions/current/",
        api_views.PrescriptionApiView.as_view(),
        name="api-prescriptions-current",
    ),
    path("api/devices/", api_views.DeviceApiView.as_view(), name="api-devices"),
    path(
        "api/infrastructure/status/",
        api_views.InfrastructureStatusApiView.as_view(),
        name="api-infrastructure-status",
    ),
]
