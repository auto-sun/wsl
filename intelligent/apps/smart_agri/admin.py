from django.contrib import admin

from .models import DeviceRecord, DiseaseDetectionRecord, OrchardBlock, PrescriptionPlan


@admin.register(OrchardBlock)
class OrchardBlockAdmin(admin.ModelAdmin):
    list_display = ("block_code", "name", "area_mu", "growth_stage", "updated_at")
    search_fields = ("block_code", "name")


@admin.register(DeviceRecord)
class DeviceRecordAdmin(admin.ModelAdmin):
    list_display = ("device_code", "name", "device_type", "status", "online", "last_seen")
    list_filter = ("device_type", "status", "online")
    search_fields = ("device_code", "name")


@admin.register(PrescriptionPlan)
class PrescriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("plan_code", "block_code", "status", "target_date", "updated_at")
    list_filter = ("status",)
    search_fields = ("plan_code", "block_code")


@admin.register(DiseaseDetectionRecord)
class DiseaseDetectionRecordAdmin(admin.ModelAdmin):
    list_display = (
        "task_code",
        "image_name",
        "plot_code",
        "disease_name",
        "confidence",
        "severity",
        "created_at",
    )
    list_filter = ("severity", "status")
    search_fields = ("task_code", "image_name", "plot_code", "disease_name")
