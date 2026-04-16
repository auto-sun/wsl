from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import DeviceCodeSerializer, DeviceCommandSerializer
from .services import DeviceService


class DeviceStatusView(APIView):
    service_class = DeviceService

    def get(self, request):
        return Response({"code": 0, "message": "ok", "data": self.service_class().get_status_payload()})


class DeviceListView(APIView):
    service_class = DeviceService

    def get(self, request):
        return Response(
            {
                "code": 0,
                "message": "ok",
                "data": self.service_class().list_devices_payload(),
            }
        )


class DeviceTestView(APIView):
    service_class = DeviceService

    def post(self, request):
        serializer = DeviceCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device_code = serializer.validated_data["device_code"]
        result = self.service_class().test_device_connection(device_code)
        if result is None:
            return Response({"code": 1, "message": "未找到对应设备", "data": {}}, status=404)

        return Response(
            {
                "code": 0,
                "message": "连接测试完成",
                "data": result,
            }
        )


class DeviceCommandView(APIView):
    service_class = DeviceService

    def post(self, request):
        serializer = DeviceCommandSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        device_code = serializer.validated_data["device_code"]
        command = serializer.validated_data.get("command") or "status_sync"
        result = self.service_class().dispatch_device_command(device_code, command)
        if result is None:
            return Response({"code": 1, "message": "未找到对应设备", "data": {}}, status=404)

        return Response(
            {
                "code": 0,
                "message": "命令已进入下发预留状态",
                "data": result,
            }
        )


class DeviceLogsView(APIView):
    service_class = DeviceService

    def get(self, request):
        device_code = request.GET.get("device_code", "")
        result = self.service_class().get_device_logs_payload(device_code)
        if result is None:
            return Response({"code": 1, "message": "未找到对应设备", "data": {}}, status=404)
        return Response(
            {
                "code": 0,
                "message": "ok",
                "data": result,
            }
        )
