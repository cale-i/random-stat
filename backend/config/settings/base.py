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
    'rest_framework_simplejwt.token_blacklist',  # Refresh Token

    # My Applications
    'estat.apps.EstatConfig',
    'apiv1.apps.Apiv1Config',
    'accounts.apps.AccountsConfig',
    'user_profile.apps.UserProfileConfig',
    'login_attempt.apps.LoginAttemptConfig',
    'auth_jwt.apps.AuthJwtConfig',
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
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
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
}
