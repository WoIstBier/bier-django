from woistbier.settings import *

#try to import secrets. this will fail if they are not there.
import woistbier.secrets as secrets
log.info('Found secrets for production settings.')
SECRET_KEY = secrets.django_secret_key

import logging
log = logging.getLogger(__name__)


#Never ever set this to True. Security risk.
DEBUG = False

ADMINS = (
  ('Admin', 'admin@woistbier.de'),
  ('Kai', 'kai@woistbier.de'),
)

ALLOWED_HOSTS = ['bier.cepheus.uberspace.de','cepheus.uberspace.de','woistbier.de','webmail.woistbier.de','mail.woistbier.de','www.woistbier.de','autoconfig.woistbier.de']

DATABASES = {
    'default': {
            'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'bier_woistbier',                      # Or path to database file if using sqlite3.
            'USER': 'bier',                      # Not used with sqlite3.
            'PASSWORD': secrets.uberspace_mysql_password,                  # Not used with sqlite3.
            'HOST': 'localhost',                     # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '3306',                     # Set to empty string for default. Not used with sqlite3.
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
        '/home/bier/django/bier/woistbier_rest/static',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)



from django.core.mail import mail_admins
import socket
print('socket.hostname : ' + socket.gethostname())
mail_admins('Server start notification', 'Hallo, \n \
                     das ist eine automatische Benarichtigung darüber, dass der Server soeben neu gestarted wurde. \n \
                     socket.hostname : ' + socket.gethostname(),  fail_silently=False);

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
