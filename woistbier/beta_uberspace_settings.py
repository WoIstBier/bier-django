from woistbier.settings import *


#try to import secrets. this will fail if they are not there.
import woistbier.secrets as secrets
log.info('Found secrets for production settings.')
SECRET_KEY = secrets.django_secret_key

#Never ever set this to True. Security risk.
DEBUG = False

HTML_ROOT_PATH='beta.woistbier.de'
ROOT_URL='beta.woistbier.de'

ADMINS = (
  # ('Admin', 'admin@woistbier.de'),
  ('Kai', 'kai@woistbier.de'),
)

ALLOWED_HOSTS = [
            'beta.bier.cepheus.uberspace.de',
            'beta.woistbier.de',
            # 'bier.cepheus.uberspace.de',
            # 'cepheus.uberspace.de',
            # 'woistbier.de',
        ]

USE_X_FORWARDED_HOST = True

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'bier_beta_woistbier',                      # Or path to database file if using sqlite3.
            'USER': 'bier',                      # Not used with sqlite3.
            'PASSWORD': secrets.uberspace_mysql_password,                  # Not used with sqlite3.
            'HOST': 'localhost',                     # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                     # Set to empty string for default. Not used with sqlite3.
            'TEST_NAME': 'bier_beta_woistbier_test_db',
            }
    }



EMAIL_HOST='localhost'
EMAIL_HOST_PASSWORD=secrets.uberspace_mail_password
EMAIL_HOST_USER='bier-admin'
EMAIL_PORT=587
EMAIL_USE_TLS=True
SERVER_EMAIL='admin@woistbier.de'



# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/var/www/virtual/bier/{}/media/'.format(HTML_ROOT_PATH)

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = 'https://{}/media/'.format(ROOT_URL)

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/www/virtual/bier/{}/static/'.format(HTML_ROOT_PATH)

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'https://{}/static/'.format(ROOT_URL)

# Additional locations of static files
STATICFILES_DIRS = (
 #       '/home/bier/bier-django/woistbier_rest/static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

REST_FRAMEWORK[ 'DEFAULT_THROTTLE_RATES'] =  {
        'kiosk_uploads': '100/minute',
        'image_uploads': '150/minute'
}


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
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/home/bier/woistbier_beta_debug.log',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
