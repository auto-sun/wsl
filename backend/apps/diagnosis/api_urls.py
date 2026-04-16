from django.urls import path

from .api_views import DiagnosisHistoryView, DiagnosisUploadView


urlpatterns = [
    path("upload", DiagnosisUploadView.as_view(), name="api-diagnosis-upload"),
    path("history", DiagnosisHistoryView.as_view(), name="api-diagnosis-history"),
]
