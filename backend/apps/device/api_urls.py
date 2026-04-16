from django.urls import path

from .api_views import (
    DeviceCommandView,
    DeviceListView,
    DeviceLogsView,
    DeviceStatusView,
    DeviceTestView,
)


urlpatterns = [
    path("status", DeviceStatusView.as_view(), name="api-device-status"),
    path("list", DeviceListView.as_view(), name="api-device-list"),
    path("test", DeviceTestView.as_view(), name="api-device-test"),
    path("command", DeviceCommandView.as_view(), name="api-device-command"),
    path("logs", DeviceLogsView.as_view(), name="api-device-logs"),
]
