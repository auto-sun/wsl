from django.urls import path

from .views import diagnosis_view


urlpatterns = [
    path("", diagnosis_view, name="diagnosis"),
]
