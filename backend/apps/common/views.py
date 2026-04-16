from django.conf import settings
from django.shortcuts import redirect, render
from rest_framework.response import Response
from rest_framework.views import APIView

from services.ai.inference import AIInferenceService
from services.cache.redis_client import RedisCacheService
from services.mqtt.client import MQTTService
from services.tsdb.influx_client import InfluxDBService
from .auth import is_demo_authenticated
from .mock_dashboard import get_dashboard_payload


def index_view(request):
    return redirect("/dashboard" if is_demo_authenticated(request) else "/login")


def dashboard_view(request):
    return render(
        request,
        "dashboard.html",
        {
            "page_title": "系统首页",
            "page_key": "dashboard",
            "page_description": "园区态势、监测总览、策略入口与设备状态预览。",
        },
    )


def api_docs_view(request):
    return render(
        request,
        "api_docs.html",
        {
            "page_title": "API 文档",
            "page_key": "api-docs",
            "page_description": "项目当前阶段已开放的页面接口、REST 接口与 mock 数据说明。",
        },
    )


def not_found_view(request, unknown_path=""):
    response = render(
        request,
        "404.html",
        {
            "page_title": "页面不存在",
            "page_key": "not-found",
            "page_description": "当前访问的页面不存在或尚未开放。",
            "unknown_path": unknown_path or request.path,
        },
    )
    response.status_code = 404
    return response


def custom_404(request, exception):
    return not_found_view(request, request.path)


class ApiRootView(APIView):
    def get(self, request):
        return Response(
            {
                "code": 0,
                "message": "ok",
                "data": {
                    "name": settings.SYSTEM_META["NAME"],
                    "phase": settings.SYSTEM_META["CURRENT_PHASE"],
                    "auth_mode": "基础登录校验占位，HTML 页面受会话保护，API 当前默认开放用于演示。",
                    "endpoints": {
                        "login": "/login",
                        "logout": "/logout",
                        "health": "/api/health",
                        "api_docs": "/api-docs",
                        "dashboard_overview": "/api/dashboard/overview",
                        "monitoring_summary": "/api/monitoring/growth-summary",
                        "monitoring_heatmap": "/api/monitoring/heatmap-data",
                        "diagnosis_upload": "/api/diagnosis/upload",
                        "diagnosis_history": "/api/diagnosis/history",
                        "decision_plans": "/api/decision/plans",
                        "decision_generate": "/api/decision/generate",
                        "decision_dispatch": "/api/decision/dispatch",
                        "devices_status": "/api/devices/status",
                        "devices_list": "/api/devices/list",
                        "devices_test": "/api/devices/test",
                        "devices_command": "/api/devices/command",
                        "dashboard": "/dashboard",
                        "monitoring": "/monitoring",
                        "diagnosis": "/diagnosis",
                        "decision": "/decision",
                        "devices": "/devices",
                    },
                },
            }
        )


class HealthView(APIView):
    def get(self, request):
        return Response(
            {
                "code": 0,
                "message": "ok",
                "data": {
                    "mysql": settings.MYSQL_CONFIG,
                    "redis": RedisCacheService().info(),
                    "influxdb": InfluxDBService().info(),
                    "mqtt": MQTTService().info(),
                    "ai": AIInferenceService().info(),
                },
            }
        )


class DashboardOverviewView(APIView):
    def get(self, request):
        return Response(
            {
                "code": 0,
                "message": "ok",
                "data": get_dashboard_payload(),
            }
        )
