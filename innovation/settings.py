# Django settings for innovation project.
import os

import dj_database_url


DIRNAME = os.path.abspath(os.path.dirname(__file__))

DEBUG = bool(os.environ.get('DEBUG', False))

DATABASES = {'default': dj_database_url.config(default='postgres://localhost/innovation')}

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

TIME_ZONE = 'Europe/London'
USE_L10N = True  # Locale
USE_TZ = True

LANGUAGE_CODE = 'en-us'
USE_I18N = False  # Internationalization

MEDIA_ROOT = os.path.join(DIRNAME, 'client_media')
MEDIA_URL = 'client_media'
STATIC_ROOT = os.path.join(DIRNAME, 'static_media')
STATIC_URL = '/static_media'

TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (os.path.join(DIRNAME, 'templates'))

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'innovation.urls'
SECRET_KEY = 'z(pw08&amp;o@5@!9gr_ni#g@v8u!mv61(8u=5$74b2-p(@+095oo='
SITE_ID = 1
WSGI_APPLICATION = 'innovation.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)

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

