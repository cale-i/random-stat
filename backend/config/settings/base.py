import os
from datetime import timedelta


#####################
#    Build paths    #
#####################
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
PROJECT_NAME = os.path.basename(BASE_DIR)

#####################
# Site Map settings #
#####################

SITE_ID = 1
SITE_EMAIL = ''
SITE_NAME = ''

#####################
# Security settings #
#####################

DEBUG = False
ALLOWED_HOSTS = []

#######################
#         CSP         #
#######################

CSP_DEFAULT_SRC = ("'none'", )
CSP_SCRIPT_SRC = ("'self'",)
CSP_IMG_SRC = ("'self'",
               'blob:',
               'data:',
               'https://random-stat.s3.amazonaws.com',
               'https://lh3.googleusercontent.com'
               )
CSP_STYLE_SRC = (
    "'self'",
    "'sha256-kwpt3lQZ21rs4cld7/uEm9qI5yAbjYzx+9FGm/XmwNU='",
)
CSP_OBJECT_SRC = ("'none'",)
CSP_PREFETCH_SRC = ("'self'",)
CSP_CONNECT_SRC = ("'self'",)
CSP_FRAME_ANCESTORS = ("'self'",)

#######################
#  Database settings  #
#######################

DATABASES = {}

#################
# Core settings #
#################

INSTALLED_APPS = [
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',

    # 3rd party apps
    'rest_framework',
    'django_filters',
    'djoser',
    'rest_framework.authtoken',  # For Account Deletion
    'django_cleanup',  # Automatically deletes old image
    'imagekit',  # For processing images
    'storages',  # django-storages
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',  # Refresh Token
    'social_django',

    # My Applications
    'estat.apps.EstatConfig',
    'apiv1.apps.Apiv1Config',
    'accounts.apps.AccountsConfig',
    'user_profile.apps.UserProfileConfig',
    'login_attempt.apps.LoginAttemptConfig',
    'auth_jwt.apps.AuthJwtConfig',
    'djoser_extend.apps.DjoserExtendConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'csp.middleware.CSPMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        }
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

#######################
# Password validation #
#######################

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

##########################
# Authenticaton Backends #
##########################

AUTHENTICATION_BACKENDS = [
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    # Django ModelBackend is the default authentication backend.
    'django.contrib.auth.backends.ModelBackend',
]

########################
# Internationalization #
########################

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

#######################
#     Static files    #
#######################

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = '/var/www/{}/static'.format(PROJECT_NAME)

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/{}/media'.format(PROJECT_NAME)


################################
#      S3 Bucket settings      #
################################

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''

#######################
#    Email Backend    #
#######################

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
DEFAULT_FROM_EMAIL = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True

######################
#   Models settings  #
######################

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
AUTH_USER_MODEL = 'accounts.CustomUser'

#################################
#     Django REST framework     #
#################################

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # Base API policies
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
}

##################
#    simplejwt   #
##################

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': (
        'rest_framework_simplejwt.tokens.AccessToken',
    ),
}

##################
#     djoser     #
##################

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': 'email/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
    'SET_USERNAME_RETYPE': True,
    'SET_PASSWORD_RETYPE': True,
    'USERNAME_RESET_CONFIRM_RETYPE': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': True,
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': True,
    'EMAIL': {
        'activation': 'djoser.email.ActivationEmail',
        'confirmation': 'djoser.email.ConfirmationEmail',
        'password_reset': 'djoser.email.PasswordResetEmail',
        'password_changed_confirmation': 'djoser.email.PasswordChangedConfirmationEmail',
        'username_changed_confirmation': 'djoser.email.UsernameChangedConfirmationEmail',
        'username_reset': 'djoser.email.UsernameResetEmail',
    },
    "LOGIN_FIELD": "email",  # Field we use to login on extended User model
    'SERIALIZERS': {},
    # Redirected URL we listen on google console
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': [],
}

##################
#   Social Auth  #
##################

# Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid',
]

# GitHub
SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''
SOCIAL_AUTH_GITHUB_SCOPE = [
    'user:email'
]

# Facebook
SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'email'
}

SOCIAL_AUTH_RAISE_EXCEPTIONS = False

# For django 3.1+
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_JSONFIELD_CUSTOM = 'django.db.models.JSONField'


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social.pipeline.user.create_user_profile',  # avatar設定
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social_core.pipeline.disconnect.allowed_to_disconnect',
    'social_core.pipeline.disconnect.get_entries',
    'social.pipeline.user.delete_social_image_url',
    'social_core.pipeline.disconnect.disconnect',
)

# SOCIAL_AUTH_REDIRECT_IS_HTTPS = True
# SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['state']
# SESSION_COOKIE_SECURE = False
