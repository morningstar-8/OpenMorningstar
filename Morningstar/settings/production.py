from .common import *
import os

"""一系列安全措施"""
# NOTE: 检测方法: python3 manage.py check --settings=Morningstar.settings.production --deploy
X_FRAME_OPTIONS = 'SAMEORIGIN'  # NOTE: 这是用来支持同源的iframe 一般用'DENY'
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True


SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = ['.morningstar529.com']


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djangodb',
        'USER': 'root',
        'PASSWORD': '1234asdw',
        'HOST': 'db1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': 'memcached:11211',
        'TIMEOUT': 60,
    },
    "redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 1000,
                "encoding": 'utf-8'
            },
            "PASSWORD": "1234asdw"
        }
    }
}

# 静态文件加速
STATIC_URL = 'https://cdn.jsdelivr.net/gh/HenryJi529/OpenMorningstarStatic@main/'

# RECAPTCHA-V2
RECAPTCHA_DOMAIN = 'www.recaptcha.net'
RECAPTCHA_PUBLIC_KEY = os.environ['RECAPTCHA_PUBLIC_KEY']
RECAPTCHA_PRIVATE_KEY = os.environ['RECAPTCHA_PRIVATE_KEY']
