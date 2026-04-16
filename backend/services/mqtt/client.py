from django.conf import settings


class MQTTService:
    def info(self):
        return {
            "enabled": False,
            "config": settings.MQTT_CONFIG,
            "message": "TODO: 接入真实 MQTT Broker 后实现设备消息订阅与控制指令下发。",
        }

    def dispatch_strategy(self, payload):
        """
        当前占位流程：
        - 仅返回模拟下发预览
        - 不向真实控制器发送命令

        未来真实接入点：
        - 对接水肥控制器
        - 对接自动灌溉执行单元
        - 通过 MQTT 下发真实控制命令并订阅回执
        """

        return {
            "accepted": False,
            "topic": f"{settings.MQTT_CONFIG['TOPIC_PREFIX']}/strategy/dispatch",
            "payload": payload,
            "message": "当前为下发预留状态，未连接真实 MQTT Broker 与控制系统。",
        }

    def dispatch_device_command(self, payload):
        return {
            "accepted": False,
            "topic": f"{settings.MQTT_CONFIG['TOPIC_PREFIX']}/device/{payload['device_code']}/command",
            "payload": payload,
            "message": "当前仅返回命令下发预览，未触发真实设备动作。",
        }
