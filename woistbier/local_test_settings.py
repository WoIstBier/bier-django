from woistbier.settings import *

import logging
log = logging.getLogger(__name__)

SECRET_KEY='pryKap1ZuB2rWCKLt913eGcb6evhiNwUQnQGvSZemnelaPtMyE'

DEBUG=True
SECURE_SSL_REDIRECT=False

log.info('Debug is set to: {}'.format(DEBUG))
log.info('SSL redirection is set to: {}'.format(SECURE_SSL_REDIRECT))

import os
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
STATIC_URL = 'http://127.0.0.1:8000/bier/static/'


ROOT_URLCONF = 'woistbier.urls'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
# NOSE_ARGS = ['--verbosity=2', '--nologcapture']
NOSE_ARGS = ['--verbosity=2']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': './local_db.sqlite',
    }
}

INSTALLED_APPS = INSTALLED_APPS + (
    'debug_toolbar',
)
MIDDLEWARE_CLASSES =  MIDDLEWARE_CLASSES + (
'debug_toolbar.middleware.DebugToolbarMiddleware',
)
INTERNAL_IPS = ('127.0.0.1',)

REST_FRAMEWORK[ 'DEFAULT_THROTTLE_RATES'] =  {
        'kiosk_uploads': '100/minute',
        'image_uploads': '150/minute'
}

log.info('Read local_test_settings. Using database: {}'.format(DATABASES))
