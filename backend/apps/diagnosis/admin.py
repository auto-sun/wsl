from django.contrib import admin

from .models import DiagnosisTask


@admin.register(DiagnosisTask)
class DiagnosisTaskAdmin(admin.ModelAdmin):
    list_display = (
        "task_code",
        "image_name",
        "diagnosis_name",
        "confidence",
        "risk_level",
        "inference_mode",
        "created_at",
    )
    search_fields = ("task_code", "image_name", "diagnosis_name")
    list_filter = ("risk_level", "inference_mode", "status")
