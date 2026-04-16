"""
项目名称：基于 AI + 无人机的火龙果长势监测与精准水肥一体化系统研发
当前阶段：PC 端 Web 单体应用，保留后续接入真实模型、MQTT、传感器与时序数据库的扩展位。
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-)z))mj2)w2=oqx$jpf_9xtvl)048f48%m%cwoqio#f0uq5u%7s",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.smart_agri",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "intelligent.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "intelligent.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DB_ENGINE = os.getenv("DB_ENGINE", "sqlite").lower()

if DB_ENGINE == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("MYSQL_DATABASE", "dragonfruit_ai"),
            "USER": os.getenv("MYSQL_USER", "root"),
            "PASSWORD": os.getenv("MYSQL_PASSWORD", "root"),
            "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
            "PORT": os.getenv("MYSQL_PORT", "3306"),
            "OPTIONS": {
                "charset": "utf8mb4",
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = os.getenv("TIME_ZONE", "Asia/Shanghai")

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "/login/"

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
}

SMART_AGRI_PROJECT = {
    "NAME": "火龙果长势监测与精准水肥一体化系统",
    "DEMO_USER": os.getenv("DEMO_USERNAME", "admin"),
    "DEMO_PASSWORD": os.getenv("DEMO_PASSWORD", "123456"),
    "DEMO_NAME": os.getenv("DEMO_NAME", "园区总控员"),
}

MYSQL_BUSINESS_CONFIG = {
    "ENGINE": DB_ENGINE,
    "DATABASE": os.getenv("MYSQL_DATABASE", "dragonfruit_ai"),
    "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "PORT": os.getenv("MYSQL_PORT", "3306"),
    "TODO": "生产环境切换 MySQL 时，请安装 mysqlclient 或兼容驱动，并补充连接池策略。",
}

INFLUXDB_CONFIG = {
    "ENABLED": os.getenv("INFLUXDB_ENABLED", "false").lower() == "true",
    "URL": os.getenv("INFLUXDB_URL", "http://127.0.0.1:8086"),
    "TOKEN": os.getenv("INFLUXDB_TOKEN", ""),
    "ORG": os.getenv("INFLUXDB_ORG", "dragonfruit-lab"),
    "BUCKET": os.getenv("INFLUXDB_BUCKET", "growth-metrics"),
    "TODO": "后续用于接入无人机巡检与传感器时序数据。",
}

REDIS_CONFIG = {
    "ENABLED": os.getenv("REDIS_ENABLED", "false").lower() == "true",
    "HOST": os.getenv("REDIS_HOST", "127.0.0.1"),
    "PORT": os.getenv("REDIS_PORT", "6379"),
    "DB": os.getenv("REDIS_DB", "0"),
    "TODO": "后续用于缓存策略结果、设备状态与异步任务状态。",
}

MQTT_CONFIG = {
    "ENABLED": os.getenv("MQTT_ENABLED", "false").lower() == "true",
    "HOST": os.getenv("MQTT_HOST", "127.0.0.1"),
    "PORT": os.getenv("MQTT_PORT", "1883"),
    "USERNAME": os.getenv("MQTT_USERNAME", ""),
    "TOPIC_PREFIX": os.getenv("MQTT_TOPIC_PREFIX", "dragonfruit/farm"),
    "TODO": "后续用于灌溉控制指令、设备心跳和传感器上报。",
}

MODEL_INFERENCE_CONFIG = {
    "ENABLED": os.getenv("MODEL_SERVICE_ENABLED", "false").lower() == "true",
    "BASE_URL": os.getenv("MODEL_SERVICE_URL", "http://127.0.0.1:9000"),
    "TIMEOUT": int(os.getenv("MODEL_SERVICE_TIMEOUT", "8")),
    "TODO": "当前仅使用 mock 检测结果，后续替换为真实病虫害识别服务。",
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
