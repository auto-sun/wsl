from django.urls import path

from .api_views import DecisionDispatchView, DecisionGenerateView, DecisionPlansView


urlpatterns = [
    path("plans", DecisionPlansView.as_view(), name="api-decision-plans"),
    path("generate", DecisionGenerateView.as_view(), name="api-decision-generate"),
    path("dispatch", DecisionDispatchView.as_view(), name="api-decision-dispatch"),
]
