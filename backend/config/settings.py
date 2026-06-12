import importlib.util
import os
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BASE_DIR.parent
FRONTEND_DIR = ROOT_DIR / "frontend"


def load_env_file(env_path):
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file(ROOT_DIR / ".env")

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-dragonfruit-platform-secret-key")
DEBUG = os.getenv("DJANGO_DEBUG", "true").lower() == "true"
ALLOWED_HOSTS = [host for host in os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost,testserver").split(",") if host]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.common",
    "apps.user",
    "apps.monitoring",
    "apps.diagnosis",
    "apps.decision",
    "apps.device",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "apps.common.middleware.DemoLoginRequiredMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ENABLE_CORS = os.getenv("ENABLE_CORS", "false").lower() == "true"
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "false").lower() == "true"
CORS_ALLOWED_ORIGINS = [item for item in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if item]

if ENABLE_CORS and importlib.util.find_spec("corsheaders"):
    INSTALLED_APPS.insert(0, "corsheaders")
    MIDDLEWARE.insert(2, "corsheaders.middleware.CorsMiddleware")

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
APPEND_SLASH = False

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [FRONTEND_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.common.context_processors.layout_context",
            ],
        },
    }
]

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()
RUNNING_TESTS = "test" in sys.argv

if DB_ENGINE == "mysql" and not RUNNING_TESTS:
    try:
        import MySQLdb  # noqa: F401
    except ImportError:
        if importlib.util.find_spec("pymysql"):
            import pymysql

            pymysql.install_as_MySQLdb()

MYSQL_CONFIG = {
    "ENGINE": "django.db.backends.mysql",
    "NAME": os.getenv("MYSQL_NAME", "dragon_fruit"),
    "USER": os.getenv("MYSQL_USER", "root"),
    "PASSWORD": os.getenv("MYSQL_PASSWORD", "12345"),
    "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "PORT": os.getenv("MYSQL_PORT", "3306"),
    "OPTIONS": {"charset": "utf8mb4"},
    "TODO": "后续切换到 MySQL 时启用该配置，并安装 mysqlclient 或兼容驱动。",
}

if DB_ENGINE == "mysql" and not RUNNING_TESTS:
    DATABASES = {"default": MYSQL_CONFIG}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "zh-hans"
TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Shanghai")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATICFILES_DIRS = [FRONTEND_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = ROOT_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

REDIS_CONFIG = {
    "HOST": os.getenv("REDIS_HOST", "127.0.0.1"),
    "PORT": os.getenv("REDIS_PORT", "6379"),
    "DB": os.getenv("REDIS_DB", "0"),
    "PASSWORD": os.getenv("REDIS_PASSWORD", ""),
    "TODO": "当前仅保留缓存配置占位，后续用于设备状态、策略结果和会话缓存。",
}

INFLUXDB_CONFIG = {
    "URL": os.getenv("INFLUXDB_URL", "http://127.0.0.1:8086"),
    "TOKEN": os.getenv("INFLUXDB_TOKEN", ""),
    "ORG": os.getenv("INFLUXDB_ORG", "dragonfruit-lab"),
    "BUCKET": os.getenv("INFLUXDB_BUCKET", "monitoring"),
    "TODO": "当前仅保留时序数据配置占位，后续接入长势曲线和传感器时序指标。",
}

MQTT_CONFIG = {
    "HOST": os.getenv("MQTT_HOST", "127.0.0.1"),
    "PORT": os.getenv("MQTT_PORT", "1883"),
    "USERNAME": os.getenv("MQTT_USERNAME", ""),
    "PASSWORD": os.getenv("MQTT_PASSWORD", ""),
    "TOPIC_PREFIX": os.getenv("MQTT_TOPIC_PREFIX", "dragonfruit/farm"),
    "TODO": "当前仅保留设备控制与消息订阅配置占位，后续接入真实 Broker。",
}

AI_SERVICE_CONFIG = {
    "BASE_URL": os.getenv("AI_SERVICE_BASE_URL", "http://127.0.0.1:9000"),
    "TIMEOUT": int(os.getenv("AI_SERVICE_TIMEOUT", "8")),
    "MODEL_PATH": os.getenv("AI_MODEL_PATH", str(ROOT_DIR / "models" / "dragonfruit_disease_yolov8s.pt")),
    "CONFIDENCE_THRESHOLD": float(os.getenv("AI_MODEL_CONFIDENCE_THRESHOLD", "0.25")),
    "IOU_THRESHOLD": float(os.getenv("AI_MODEL_IOU_THRESHOLD", "0.45")),
    "IMAGE_SIZE": int(os.getenv("AI_MODEL_IMAGE_SIZE", "640")),
    "DEVICE": os.getenv("AI_MODEL_DEVICE", "cpu"),
    "FALLBACK_TO_MOCK": os.getenv("AI_MODEL_FALLBACK_TO_MOCK", "true").lower() == "true",
    "TODO": "病虫害检测优先读取本地 YOLOv8 权重；未放置模型或推理异常时可按配置回退 mock。",
}

SYSTEM_META = {
    "NAME": "火龙果智慧管控平台",
    "SUBTITLE": "基于 AI + 无人机的火龙果长势监测与精准水肥一体化系统",
    "CURRENT_PHASE": "第一阶段：单体脚手架、页面骨架、API 占位与扩展接口预留",
}

ADMIN_INVITE_CODE = os.getenv("ADMIN_INVITE_CODE", "liyang")
