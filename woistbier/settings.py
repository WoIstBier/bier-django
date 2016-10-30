#use pymysql
import pymysql
pymysql.install_as_MySQLdb()

#Global  Django settings for woistbier project.
import logging
logging.basicConfig(level=logging.DEBUG)
log= logging.getLogger(__name__)
log.info('Reading Settings!')


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'de'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

SESSION_COOKIE_SECURE=True

CSRF_COOKIE_SECURE=True

CSRF_COOKIE_HTTPONLY=True

SECURE_CONTENT_TYPE_NOSNIFF=True

SECURE_BROWSER_XSS_FILTER=True

X_FRAME_OPTIONS='DENY'

# this should be set at some point
# SECURE_SSL_REDIRECT=True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'woistbier.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'woistbier.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'easy_thumbnails',
    'woistbier_rest',
    'django_nose',
    'rest_framework'
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


THUMBNAIL_ALIASES = {
    '': {
        'thumbnail': {'size': (64, 64), 'crop': "smart"},
        'gallery': {'size': (640, 480), 'autocrop':"True"},
        'medium': {'size': (140, 120), 'crop': "smart"},
    },
}

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
