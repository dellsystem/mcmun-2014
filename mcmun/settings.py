import django.conf.global_settings as DEFAULT_SETTINGS
import djcelery
import logging

from mcmun import conf


DEBUG = conf.DEBUG
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = (
	'127.0.0.1',
)

ALLOWED_HOSTS = conf.ALLOWED_HOSTS

ADMINS = (
    ('IT', 'it@mcmun.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': conf.DB_ENGINE,
        'NAME': conf.DB_NAME,
        'USER': conf.DB_USER,
        'PASSWORD': conf.DB_PASSWORD,
        'HOST': conf.DB_HOST,
        'PORT': conf.DB_PORT,
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = conf.MEDIA_ROOT

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = conf.STATIC_ROOT

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

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
SECRET_KEY = conf.SECRET_KEY

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

ROOT_URLCONF = 'mcmun.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'mcmun.wsgi.application'

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
    'django.contrib.markup',
    'committees',
    'cms',
    'signups',
    'mcmun',
    'django.contrib.admin',
    'djcelery',
    'djcelery.transport',
    'staffapps',
    'search',
    'merchandise',
) + conf.INSTALLED_APPS

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    "cms.context_processors.menu",
    "committees.context_processors.committees",
)

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'it@mcmun.org'
EMAIL_HOST_PASSWORD = conf.EMAIL_PASSWORD

IT_EMAIL = 'it@mcmun.org'
CHARGE_EMAIL = 'chargee@mcmun.org'
FINANCE_EMAIL = 'finance@mcmun.org'

ADMIN_URL = 'http://www.mcmun.org/%s/' % conf.ADMIN_PREFIX

CSRF_COOKIE_DOMAIN = conf.COOKIE_DOMAIN
DEFAULT_FROM_EMAIL = 'it@mcmun.org'

logging.getLogger('xhtml2pdf')

djcelery.setup_loader()
BROKER_URL = 'django://'
CELERY_RESULT_BACKEND = "database"
CELERY_RESULT_DBURI = "sqlite:///db.sqlite"

LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/dashboard'

SEARCH_MODELS = (
    ('cms.Page', ['long_name', 'content']),
    ('committees.Committee', ['name', 'description']),
    ('mcmun.SecretariatMember', ['name', 'position', 'bio']),
)
