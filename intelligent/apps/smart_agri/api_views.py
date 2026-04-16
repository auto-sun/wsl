import os
import uuid

from django.conf import settings
from django.core.files.storage import default_storage
from django.utils import timezone
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from .models import DiseaseDetectionRecord
from .serializers import DetectionUploadSerializer, LoginSerializer
from .services.infrastructure import (
    ModelInferenceService,
    MQTTGatewayService,
    get_infrastructure_status,
)
from .services.mock_data import (
    build_detection_result,
    get_dashboard_payload,
    get_demo_user,
    get_device_payload,
    get_growth_heatmap_geojson,
    get_growth_payload,
    get_prescription_payload,
    get_recent_detection_history,
)
from .utils import api_error, api_success
from .views import SESSION_FLAG, SESSION_USER_KEY


class SessionProtectedAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        if not request.session.get(SESSION_FLAG):
            return api_error("请先登录系统。", status_code=status.HTTP_401_UNAUTHORIZED)
        return super().dispatch(request, *args, **kwargs)


class LoginApiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        credentials = serializer.validated_data
        demo_user = get_demo_user()
        if (
            credentials["username"] != demo_user["username"]
            or credentials["password"] != demo_user["password"]
        ):
            return api_error("账号或密码错误，请使用演示账号登录。", status_code=400)

        request.session[SESSION_FLAG] = True
        request.session[SESSION_USER_KEY] = {
            "username": demo_user["username"],
            "display_name": demo_user["display_name"],
            "role": demo_user["role"],
        }
        request.session["login_at"] = timezone.now().isoformat()
        request.session.cycle_key()
        return api_success(
            {
                "redirect": "/dashboard/",
                "user": request.session[SESSION_USER_KEY],
            },
            message="登录成功",
        )


class LogoutApiView(SessionProtectedAPIView):
    def post(self, request):
        request.session.flush()
        return api_success({"redirect": "/login/"}, message="已退出登录")


class DashboardOverviewApiView(SessionProtectedAPIView):
    def get(self, request):
        payload = get_dashboard_payload()
        payload["user"] = request.session.get(SESSION_USER_KEY, {})
        return api_success(payload)


class GrowthSummaryApiView(SessionProtectedAPIView):
    def get(self, request):
        return api_success(get_growth_payload())


class GrowthHeatmapApiView(SessionProtectedAPIView):
    def get(self, request):
        return api_success(
            {
                "map": {
                    "center": get_dashboard_payload()["map"]["center"],
                    "zoom": get_dashboard_payload()["map"]["zoom"],
                },
                "geojson": get_growth_heatmap_geojson(),
            }
        )


class DiseaseDetectionApiView(SessionProtectedAPIView):
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        records = DiseaseDetectionRecord.objects.all()[:8]
        history = [
            {
                "task_code": item.task_code,
                "image_name": item.image_name,
                "plot_code": item.plot_code,
                "disease_name": item.disease_name,
                "severity": item.severity,
                "confidence": item.confidence,
                "created_at": timezone.localtime(item.created_at).strftime("%Y-%m-%d %H:%M"),
            }
            for item in records
        ]
        if not history:
            history = get_recent_detection_history()
        return api_success({"history": history})

    def post(self, request):
        serializer = DetectionUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploaded_file = serializer.validated_data["image"]
        plot_code = serializer.validated_data.get("plot_code", "")

        extension = os.path.splitext(uploaded_file.name)[1] or ".jpg"
        stored_name = default_storage.save(
            f"detections/{timezone.now().strftime('%Y%m%d')}/{uuid.uuid4().hex}{extension}",
            uploaded_file,
        )
        result = build_detection_result(
            file_name=uploaded_file.name,
            file_size=uploaded_file.size,
            plot_code=plot_code,
        )

        DiseaseDetectionRecord.objects.create(
            task_code=result["task_code"],
            image_name=uploaded_file.name,
            stored_path=stored_name,
            plot_code=result["plot_code"],
            disease_name=result["disease_name"],
            confidence=result["confidence"],
            severity=result["severity"],
            result_payload=result,
        )

        result["storage_path"] = stored_name
        result["inference"] = ModelInferenceService().infer_disease(stored_name)
        return api_success(result, message="检测完成")


class PrescriptionApiView(SessionProtectedAPIView):
    def get(self, request):
        payload = get_prescription_payload()
        payload["dispatch_preview"] = MQTTGatewayService().publish_irrigation_plan(
            {"plan_code": "PREVIEW-20260410", "zones": payload["zones"]}
        )
        return api_success(payload)


class DeviceApiView(SessionProtectedAPIView):
    def get(self, request):
        payload = get_device_payload()
        payload["infrastructure"] = get_infrastructure_status()
        return api_success(payload)


class InfrastructureStatusApiView(SessionProtectedAPIView):
    def get(self, request):
        return api_success(get_infrastructure_status())
