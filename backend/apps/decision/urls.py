from django.urls import path

from .views import decision_view


urlpatterns = [
    path("", decision_view, name="decision"),
]
