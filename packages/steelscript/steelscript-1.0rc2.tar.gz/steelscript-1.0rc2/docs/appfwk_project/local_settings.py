
from steelscript.appfwk.project.settings import *

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATAHOME = os.getenv('DATAHOME', PROJECT_ROOT)
DATA_CACHE = os.path.join(DATAHOME, 'data', 'datacache')
INITIAL_DATA = os.path.join(DATAHOME, 'data', 'initial_data')
REPORTS_DIR = os.path.join(PROJECT_ROOT, 'reports')

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_ROOT = DATA_CACHE

# Optionally add additional applications specific to this project instance

LOCAL_APPS = (
    # additional apps can be listed here
)
INSTALLED_APPS += LOCAL_APPS

# Configure database for development or production.

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',

        # Path to database file if using sqlite3.
        # Database name for others
        'NAME': os.path.join(DATAHOME, 'data', 'project.db'),

        'USER': '',     # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '',     # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',     # Set to empty string for default. Not used with sqlite3.
    }
}

# Setup loggers to local directory
LOGGING['handlers']['logfile']['filename'] = os.path.join(DATAHOME, 'logs', 'log.txt')
LOGGING['handlers']['backend-log']['filename'] = os.path.join(DATAHOME, 'logs', 'log-db.txt')

# To enable syslog handling instead of local logging, uncomment next block of LOGGING
# statements

# remove these loggers since the configuration will attempt to write the
# files even if they don't have a logger declared for them
#LOGGING['disable_existing_loggers'] = True
#LOGGING['handlers'].pop('logfile')
#LOGGING['handlers'].pop('backend-log')
#
#LOGGING['handlers']['syslog'] = {
#    'level': 'DEBUG',
#    'class': 'logging.handlers.SysLogHandler',
#    'formatter': 'standard_syslog',
#    'facility': SysLogHandler.LOG_USER,
#    'address': '/var/run/syslog' if sys.platform == 'darwin' else '/dev/log'
#}
#
#LOGGING['loggers'] = {
#    'django.db.backends': {
#        'handlers': ['null'],
#        'level': 'DEBUG',
#        'propagate': False,
#    },
#    '': {
#        'handlers': ['syslog'],
#        'level': 'INFO',
#        'propagate': True,
#    },
#}

SECRET_KEY = '!8g*_djnc)i%6xp$1%84(dob980llzx*x=#w#f)vu2wch9&%c5'

# Add other settings customizations below, which will be local to this
# machine only, and not recorded by git. This could include database or
# other authentications, LDAP settings, or any other overrides.

# For example LDAP configurations, see the file
# `project/ldap_example.py`.
