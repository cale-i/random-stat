import environ

from .base import *

# Read .env if exists
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


#####################
# Site Map settings #
#####################

SITE_EMAIL = env('SITE_EMAIL')
SITE_NAME = 'Random Stat'
DOMAIN = 'random-stat.work'

#####################
# Security settings #
#####################

DEBUG = False
SECRET_KEY = env('SECRET_KEY')
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

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


#################################
#     Django REST framework     #
#################################

#######################
#     Guest Login     #
#######################

GUEST_EMAIL = env('GUEST_EMAIL')
GUEST_PASSWORD = env('GUEST_PASSWORD')

#######################
#   Cookie Settings   #
#######################

JWT_COOKIE = {
    'SAMESITE': 'Strict',
    # 'SECURE': True, 本番時 True
    'SECURE': False,
}

#######################
#        djoser       #
#######################
DJOSER['SOCIAL_AUTH_ALLOWED_REDIRECT_URIS'] = [
    'https://random-stat.work/social/o/google-oauth2/',
    'https://random-stat.work/social/o/github/',
    'https://random-stat.work/social/o/facebook/',
    'http://localhost/social/o/google-oauth2/',
    'http://localhost/social/o/github/',
    'http://localhost/social/o/facebook/',
]

##################
#   Social Auth  #
##################

# Google
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = env('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = env('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
SOCIAL_AUTH_GITHUB_KEY = env('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = env('SOCIAL_AUTH_GITHUB_SECRET')
SOCIAL_AUTH_FACEBOOK_KEY = env('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = env('SOCIAL_AUTH_FACEBOOK_SECRET')
