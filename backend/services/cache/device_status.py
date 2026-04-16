from django.conf import settings


class DeviceStatusService:
    """
    设备状态服务占位。

    当前阶段：
    - 仅输出缓存 key 约定和轮询扩展说明
    - 不连接 Redis，不缓存真实设备状态

    后续阶段：
    - 以 Redis 作为设备状态缓存
    - 将 MQTT 心跳、设备状态、告警摘要写入缓存
    - 为 WebSocket 或 SSE 推送提供统一数据源
    """

    def info(self):
        return {
            "enabled": False,
            "cache_backend": "Redis 预留",
            "redis_host": settings.REDIS_CONFIG["HOST"],
            "key_patterns": [
                "device:status:<device_code>",
                "device:heartbeat:<device_code>",
                "device:alert:<device_code>",
            ],
            "message": "当前未接真实设备状态缓存，未来可基于 Redis 实现实时状态同步。",
        }
