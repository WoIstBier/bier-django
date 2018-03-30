from .settings import *
import os
import logging

log = logging.getLogger(__name__)

SECRET_KEY='pryKap1ZuB2rWCKLt913eGcb6evhiNwUQnQGvSZemnelaPtMyE'

DEBUG = False if os.environ.get('DEBUG') == 'False' else True
SECURE_SSL_REDIRECT = False
print('Debug is set to: {}'.format(DEBUG))
print(type(DEBUG))
log.info('Debug is set to: {}'.format(DEBUG))
log.info('SSL redirection is set to: {}'.format(SECURE_SSL_REDIRECT))


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR,'./media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'http://127.0.0.1:8000/bier/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, '../woistbier_rest/static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


ROOT_URLCONF = 'woistbier.urls'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': './local_db.sqlite',
    }
}

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ('127.0.0.1',)

REST_FRAMEWORK[ 'DEFAULT_THROTTLE_RATES'] =  {
        'kiosk_uploads': '100/minute',
        'image_uploads': '150/minute'
}

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'standard': {
#             'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
#             'datefmt' : "%d/%b/%Y %H:%M:%S"
#         },
#     },
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console'],
#             'level': os.environ.get('LEVEL', 'WARN'),
#             'propagate': True,
#         },
#     },
# }


ALLOWED_HOSTS = [
            '0.0.0.0',
            '127.0.0.1',
            # 'bier.cepheus.uberspace.de',
            # 'cepheus.uberspace.de',
            # 'woistbier.de',
        ]

log.info('Read local_test_settings. Using database: {}'.format(DATABASES))
