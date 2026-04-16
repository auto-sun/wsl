from dataclasses import dataclass

from django.conf import settings


@dataclass
class PlaceholderServiceStatus:
    name: str
    enabled: bool
    summary: str
    todo: str

    def to_dict(self):
        return {
            "name": self.name,
            "enabled": self.enabled,
            "summary": self.summary,
            "todo": self.todo,
        }


class MQTTGatewayService:
    def __init__(self):
        self.config = settings.MQTT_CONFIG

    def health(self):
        return PlaceholderServiceStatus(
            name="MQTT 控制网关",
            enabled=self.config["ENABLED"],
            summary=f'{self.config["HOST"]}:{self.config["PORT"]}',
            todo=self.config["TODO"],
        ).to_dict()

    def publish_irrigation_plan(self, plan_payload):
        return {
            "accepted": False,
            "channel": f'{self.config["TOPIC_PREFIX"]}/irrigation/command',
            "payload": plan_payload,
            "message": "TODO: 接入真实 MQTT Broker 后再下发控制指令。",
        }


class SensorGatewayService:
    def health(self):
        return {
            "name": "传感器采集网关",
            "enabled": False,
            "summary": "当前阶段未接真实土壤湿度、温湿度和EC传感器。",
            "todo": "TODO: 接入边缘网关或串口/HTTP 数据采集模块。",
        }

    def latest_snapshot(self):
        return {
            "connected": False,
            "message": "TODO: 接入真实传感器数据流。",
        }


class InfluxDBService:
    def __init__(self):
        self.config = settings.INFLUXDB_CONFIG

    def health(self):
        return PlaceholderServiceStatus(
            name="InfluxDB 时序服务",
            enabled=self.config["ENABLED"],
            summary=self.config["URL"],
            todo=self.config["TODO"],
        ).to_dict()

    def query_growth_series(self, measurement, filters=None):
        return {
            "measurement": measurement,
            "filters": filters or {},
            "series": [],
            "message": "TODO: 接入时序数据库后返回真实曲线。",
        }


class RedisCacheService:
    def __init__(self):
        self.config = settings.REDIS_CONFIG

    def health(self):
        return PlaceholderServiceStatus(
            name="Redis 缓存服务",
            enabled=self.config["ENABLED"],
            summary=f'{self.config["HOST"]}:{self.config["PORT"]}/{self.config["DB"]}',
            todo=self.config["TODO"],
        ).to_dict()

    def cache_strategy(self, key, payload):
        return {
            "cached": False,
            "key": key,
            "payload": payload,
            "message": "TODO: 接入 Redis 后缓存策略快照与设备态势。",
        }


class ModelInferenceService:
    def __init__(self):
        self.config = settings.MODEL_INFERENCE_CONFIG

    def health(self):
        return PlaceholderServiceStatus(
            name="病虫害推理服务",
            enabled=self.config["ENABLED"],
            summary=self.config["BASE_URL"],
            todo=self.config["TODO"],
        ).to_dict()

    def infer_disease(self, file_path):
        return {
            "accepted": False,
            "file_path": file_path,
            "message": "TODO: 接入真实病虫害模型推理服务。",
        }


def get_infrastructure_status():
    return {
        "mysql": settings.MYSQL_BUSINESS_CONFIG,
        "services": [
            MQTTGatewayService().health(),
            SensorGatewayService().health(),
            InfluxDBService().health(),
            RedisCacheService().health(),
            ModelInferenceService().health(),
        ],
    }
