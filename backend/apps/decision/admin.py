from django.contrib import admin

from .models import DecisionPlan


@admin.register(DecisionPlan)
class DecisionPlanAdmin(admin.ModelAdmin):
    list_display = (
        "plan_code",
        "block_code",
        "block_name",
        "prescription_grade",
        "irrigation_amount",
        "fertilizer_amount",
        "status",
        "source_mode",
        "created_at",
    )
    search_fields = ("plan_code", "block_code", "block_name")
    list_filter = ("prescription_grade", "status", "source_mode")
