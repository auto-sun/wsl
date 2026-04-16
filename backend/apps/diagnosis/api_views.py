from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DiagnosisUploadSerializer
from .services import DiagnosisService


class DiagnosisUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    service_class = DiagnosisService

    def post(self, request):
        serializer = DiagnosisUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = self.service_class().create_diagnosis_task(
            upload_file=serializer.validated_data["image"],
            request=request,
        )
        return Response({"code": 0, "message": "检测完成", "data": result})


class DiagnosisHistoryView(APIView):
    service_class = DiagnosisService

    def get(self, request):
        return Response(
            {
                "code": 0,
                "message": "ok",
                "data": self.service_class().get_history_payload(),
            }
        )
