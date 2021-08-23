import environ

from .base import *

# Read .env if exists
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


#####################
# Security settings #
#####################

DEBUG = False

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

#####################
# Site Map settings #
#####################

SITE_EMAIL = env('SITE_EMAIL')
SITE_NAME = 'Random Stat'
DOMAIN = 'random-stat.work'

############
# Database #
############

DATABASES = {
    'default': env.db()
}
DATABASES['default']['ATOMIC_REQUESTS'] = True


##################
# REST Framework #
##################

##################
#     MEDIA      #
##################

################################
#      S3 Bucket settings      #
################################


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')

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


###################
# Cookie Settings #
###################
JWT_COOKIE = {
    'SAMESITE': 'Strict',
    # 'SECURE': True, 本番時 True
    'SECURE': False,
}
