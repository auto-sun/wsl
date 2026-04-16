from django.urls import path

from .views import devices_view


urlpatterns = [
    path("", devices_view, name="devices"),
]
