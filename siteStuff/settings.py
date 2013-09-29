# Django settings for siteStuff project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
  ('admin', 'admin@woistbier.de'),
#  ('Kai', 'kai@woistbier.de'),
)

#MANAGERS = ADMINS
ALLOWED_HOSTS = ['bier.cepheus.uberspace.de','cepheus.uberspace.de','woistbier.de','www.woistbier.de','autoconfig.woistbier.de']

import sys
# is ./manage.py test ?
TEST = 'test' in sys.argv
if TEST:
    # in-memory SQLite used for testing
    SOUTH_TESTS_MIGRATE = False
    DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'test_db',
                }
            }
    print("-------------Using test DB. Local sqlite file!!----------------")    

else:
    DATABASES = {
    	'default': {
        	'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        	'NAME': 'bier',                      # Or path to database file if using sqlite3.
        	'USER': 'bier',                      # Not used with sqlite3.
        	'PASSWORD': 'cuwakotJeonyeuvjest',                  # Not used with sqlite3.
        	'HOST': 'localhost',                     # Set to empty string for localhost. Not used with sqlite3.
        	'PORT': '3306',                     # Set to empty string for default. Not used with sqlite3.
    		}
	}

EMAIL_HOST='localhost'
EMAIL_HOST_PASSWORD='wng3x3fAYjVw'
EMAIL_HOST_USER='bier-admin'
EMAIL_PORT=587
EMAIL_USE_TLS=True
SERVER_EMAIL='admin@woistbier.de'

print('------------------------ Settings so far are: -------------')
import socket
print('Allowed hosts are: ' + str(ALLOWED_HOSTS) + '  socket.hostname : ' + socket.gethostname())
print('admins: ' + str(ADMINS))

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

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/var/www/virtual/bier/html/bier/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/bier/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/virtual/bier/html/bier/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/bier/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-e8_!iy!jknm!%sxw$8=a5t#^t=lzctijb=t@djup(t$hhs^)+'

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
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'siteStuff.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'siteStuff.wsgi.application'

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
    # 'django.contrib.admindocs',
    'bier',
    'south',
    'rest_framework',
    'easy_thumbnails'
)
THUMBNAIL_ALIASES = {
    '': {
        'thumbnail': {'size': (64, 64), 'crop': "smart"},
        'gallery': {'size': (640, 480), 'crop': "smart"},
        'medium': {'size': (140, 120), 'crop': "smart"},
    },
}


REST_FRAMEWORK = {
    'FILTER_BACKEND': 'rest_framework.filters.DjangoFilterBackend'
}

from django.core.mail import mail_admins
import socket
print('socket.hostname : ' + socket.gethostname())
mail_admins('Server Started', 'Read settings.py. This means the server has been started \n socket.hostname : ' + socket.gethostname(),  fail_silently=False);

#from django.core.mail import send_mail
#send_mail('Subject here', 'Here is the message.', 'admin@woistbier.de', ['admin@woistbier.de'], fail_silently=False)
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': "/home/bier/" + "logfile-django.log",
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
          }
    },
    'loggers': {
        'django': {
            'handlers':['console', 'logfile', 'mail_admins'],
            'propagate': True,
            'level':'WARN',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
	},
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
	'bier':{
	    'handlers': ['console', 'logfile','mail_admins'],
            'level': 'DEBUG',
            },
        '': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
    }
}
