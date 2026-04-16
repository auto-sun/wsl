from django.conf import settings


class RedisCacheService:
    def info(self):
        return {
            "enabled": False,
            "config": settings.REDIS_CONFIG,
            "message": "TODO: 接入 Redis 后缓存设备状态、处方结果和热区摘要。",
        }
