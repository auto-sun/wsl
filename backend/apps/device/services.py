from services.cache.device_status import DeviceStatusService
from services.mqtt.client import MQTTService
from services.mqtt.topics import get_device_topic_contract

from .mock_data import get_device, get_devices, get_logs, get_status_payload


class DeviceService:
    """
    设备管理服务。

    当前阶段：
    - 统一封装设备状态、日志、连接测试、命令下发占位
    - 使用 mock 数据驱动页面与 API

    未来阶段：
    - 可接入真实设备注册表、MQTT 状态订阅、Redis 实时缓存、WebSocket 推送
    """

    def __init__(self, mqtt_service=None, device_status_service=None):
        self.mqtt_service = mqtt_service or MQTTService()
        self.device_status_service = device_status_service or DeviceStatusService()

    def get_status_payload(self):
        payload = get_status_payload()
        payload["extensions"] = {
            "device_status_service": self.device_status_service.info(),
            "mqtt_topics": get_device_topic_contract(),
            "realtime_push": {
                "current_mode": "mock + 轮询",
                "polling_endpoint": "/api/devices/status",
                "websocket_placeholder": "/ws/devices/status/",
                "message": "当前未启用真实 WebSocket 推送，后续可在设备状态 service 上扩展轮询或实时订阅。",
            },
        }
        return payload

    def list_devices_payload(self):
        return {
            "devices": get_devices(),
            "boundary_notice": "当前设备数据均为 mock 数据，不代表真实硬件在线状态。",
        }

    def test_device_connection(self, device_code):
        device = get_device(device_code)
        if device is None:
            return None

        return {
            "device_code": device_code,
            "result": "测试完成",
            "success": device["online"],
            "message": "当前为 mock 连接测试，未与真实硬件建立通信。",
        }

    def dispatch_device_command(self, device_code, command):
        device = get_device(device_code)
        if device is None:
            return None

        preview = self.mqtt_service.dispatch_device_command(
            {
                "device_code": device_code,
                "command": command,
            }
        )
        return {
            "device_code": device_code,
            "command": command,
            "preview": preview,
            "message": "当前未接真实硬件，不会执行真实控制。",
        }

    def get_device_logs_payload(self, device_code):
        device = get_device(device_code)
        if device is None:
            return None

        return {
            "device_code": device_code,
            "logs": get_logs(device_code),
            "message": "当前为 mock 日志输出，未接入真实设备日志采集。",
        }
