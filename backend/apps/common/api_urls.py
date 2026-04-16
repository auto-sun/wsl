from django.urls import path

from .views import ApiRootView, DashboardOverviewView, HealthView


urlpatterns = [
    path("", ApiRootView.as_view(), name="api-root"),
    path("health", HealthView.as_view(), name="api-health"),
    path("dashboard/overview", DashboardOverviewView.as_view(), name="api-dashboard-overview"),
]
