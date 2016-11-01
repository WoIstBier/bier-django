from woistbier.settings import *

import logging
log = logging.getLogger(__name__)

SECRET_KEY='pryKap1ZuB2rWCKLt913eGcb6evhiNwUQnQGvSZemnelaPtMyE'

DEBUG=True

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR,'./media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/bier/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, '../woistbier_rest/static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/bier/static/'

# Additional locations of static files
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, './static/'),
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)


ROOT_URLCONF = 'woistbier.urls'

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
#NOSE_ARGS = ['--verbosity=2', '--nologcapture']
NOSE_ARGS = ['--verbosity=2']


REST_FRAMEWORK = {
    'FILTER_BACKEND': 'rest_framework.filters.DjangoFilterBackend',

    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'kiosk_uploads': '10/minute',
        'image_uploads': '15/minute'
    }
}

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

log.info('Read local_test_settings. Using database: {}'.format(DATABASES))
