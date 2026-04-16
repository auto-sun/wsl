from django.conf import settings


class InfluxDBService:
    def info(self):
        return {
            "enabled": False,
            "config": settings.INFLUXDB_CONFIG,
            "message": "TODO: 接入 InfluxDB 后承载传感器、巡检时序和告警指标。",
        }
