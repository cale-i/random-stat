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
# Site Map settings #
#####################

SITE_EMAIL = env('SITE_EMAIL')
SITE_NAME = 'http://localhost:8000'
DOMAIN = 'localhost:8000'  # Used for email confirmation URL

#####################
# Security settings #
#####################

DEBUG = True
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

######################
#   CORS settings    #
######################

CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:8080',
    'http://127.0.0.1:8080',
)

#######################
#  Database settings  #
#######################

DATABASES = {
    'default': env.db()
}
DATABASES['default']['ATOMIC_REQUESTS'] = False

#######################
#     Static files    #
#######################

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

################################
#      S3 Bucket settings      #
################################

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

#######################
#    Email Backend    #
#######################

EMAIL_HOST_USER = env('SITE_EMAIL')
DEFAULT_FROM_EMAIL = env('SITE_EMAIL')
EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')

#######################
#       Logging       #
#######################

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

#######################
#    debug toolbar    #
#######################

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


#################################
#     Django REST framework     #
#################################

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += [
    'rest_framework.renderers.BrowsableAPIRenderer']

#######################
#     Guest Login     #
#######################

GUEST_EMAIL = env('GUEST_EMAIL')
GUEST_PASSWORD = env('GUEST_PASSWORD')

#######################
#   Cookie Settings   #
#######################

JWT_COOKIE = {
    'SAMESITE': 'Lax',
    'SECURE': False,
}

##################
#   Social Auth  #
##################

# Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GITHUB_KEY = env('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = env('SOCIAL_AUTH_GITHUB_SECRET')
SOCIAL_AUTH_FACEBOOK_KEY = env('SOCIAL_AUTH_FACEBOOK_KEY_LOCAL')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET_LOCAL')
