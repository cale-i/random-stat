import environ
import os

from .base import *
from .base import (
    BASE_DIR,
    INSTALLED_APPS,
    MIDDLEWARE,
    REST_FRAMEWORK
)


# Read .env if exists
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


#####################
# Security settings #
#####################

DEBUG = True

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

#####################
# Site Map settings #
#####################

SITE_EMAIL = env('SITE_EMAIL')
SITE_NAME = 'http://localhost:8080'
DOMAIN = 'localhost:8080'

############
# Database #
############

DATABASES = {
    'default': env.db()
}
DATABASES['default']['ATOMIC_REQUESTS'] = True

###########
# Logging #
###########

LOGGING = {
    # バージョンは「1」固定
    'version': 1,
    # 既存のログ設定を無効化しない
    'disable_existing_loggers': False,
    # ログフォーマット
    'formatters': {
        # 開発用
        'develop': {
            'format': '%(asctime)s [%(levelname)s] %(pathname)s:%(lineno)d '
                      '%(message)s'
        },
    },
    # ハンドラ
    'handlers': {
        # コンソール出力用ハンドラ
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'develop',
        },
    },
    # ロガー
    'loggers': {
        # 自作アプリケーション全般のログを拾うロガー
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        # Django本体が出すログ全般を拾うロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # 発行されるSQL文を出力するための設定
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        #     'propagate': False,
        # },
    },
}


################
# Static files #
################

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

################################
#      S3 Bucket settings      #
################################


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

#################
# debug toolbar #
#################

if DEBUG:
    def show_toolbar(request):
        return True

    INSTALLED_APPS += (
        'debug_toolbar',
    )
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': show_toolbar,
    }


########
# CORS #
########

INSTALLED_APPS += [
    'corsheaders',
]

MIDDLEWARE += [
    'corsheaders.middleware.CorsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',
    'http://127.0.0.1:8080',
)

###################
# Cookie Settings #
###################
JWT_COOKIE = {
    'SAMESITE': 'None',
    'SECURE': False,
}


##################
# REST Framework #
##################

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += [
    'rest_framework.renderers.BrowsableAPIRenderer']

#################
# Email Backend #
#################

EMAIL_HOST_USER = env('SITE_EMAIL')
DEFAULT_FROM_EMAIL = env('SITE_EMAIL')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')

#################
#  Guest Login  #
#################
GUEST_EMAIL = env('GUEST_EMAIL')
GUEST_PASSWORD = env('GUEST_PASSWORD')
