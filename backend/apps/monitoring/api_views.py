from rest_framework.response import Response
from rest_framework.views import APIView

from .services import MonitoringService


class GrowthSummaryView(APIView):
    service_class = MonitoringService

    def get(self, request):
        return Response(
            {
                "code": 0,
                "message": "ok",
                "data": self.service_class().get_growth_summary_payload(),
            }
        )


class HeatmapDataView(APIView):
    service_class = MonitoringService

    def get(self, request):
        return Response(
            {
                "code": 0,
                "message": "ok",
                "data": self.service_class().get_heatmap_payload(),
            }
        )
