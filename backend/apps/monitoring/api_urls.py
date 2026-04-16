from django.urls import path

from .api_views import GrowthSummaryView, HeatmapDataView


urlpatterns = [
    path("growth-summary", GrowthSummaryView.as_view(), name="api-growth-summary"),
    path("heatmap-data", HeatmapDataView.as_view(), name="api-heatmap-data"),
]
