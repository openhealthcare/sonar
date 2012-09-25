# Django settings for innovation project.
import os

import dj_database_url


DIRNAME = os.path.abspath(os.path.dirname(__file__))

DEBUG = bool(os.environ.get('DEBUG', False))

# DATABASES = {'default': dj_database_url.config(default='postgres://localhost/innovation')}
DATABASES = {'default': dj_database_url.config(default='sqlite:///%s/innovation.db' % DIRNAME)}

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
if not DEBUG:
    EMAIL_HOST_USER = os.environ['SENDGRID_USERNAME']
    EMAIL_HOST= 'smtp.sendgrid.net'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_PASSWORD = os.environ['SENDGRID_PASSWORD']
else:
    EMAIL_PORT = 1025
    EMAIL_HOST = 'localhost'


# DEFAULT_FROM_EMAIL is for email confirmation from the Django allauth module
DEFAULT_FROM_EMAIL = 'do-not-reply@innovation_r_us.nhs.gov.uk'

TIME_ZONE = 'Europe/London'
USE_L10N = True  # Locale
USE_TZ = True

LANGUAGE_CODE = 'en-us'
USE_I18N = False  # Internationalization

MEDIA_ROOT = os.path.join(DIRNAME, 'client_media')
MEDIA_URL = '/client_media/'
STATIC_ROOT = os.path.join(DIRNAME, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "/admin/"

TEMPLATE_DEBUG = DEBUG
TEMPLATE_DIRS = (os.path.join(DIRNAME, 'templates'))

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'innovation.middleware.LogException',
)

ROOT_URLCONF = 'innovation.urls'

TEMPLATE_CONTEXT_PROCESSORS = (
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'innovation.context_processors.recent',
)

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Allauth options
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/accounts/login'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[NHS Innovation Portal] '
ACCOUNT_EMAIL_VERIFICATION = False
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
CONTACT_EMAIL = DEFAULT_FROM_EMAIL
LOGIN_REDIRECT_URL = '/'


SECRET_KEY = 'z(pw08&amp;o@5@!9gr_ni#g@v8u!mv61(8u=5$74b2-p(@+095oo='
SITE_ID = 1
WSGI_APPLICATION = 'innovation.wsgi.application'

INSTALLED_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'bootstrapform',
    'profiles',
    'uni_form',
    'taggit',
    'filebrowser',
    # 'allauth.socialaccount.providers.google',
    # 'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.linkedin',
    # 'allauth.socialaccount.providers.openid',
    # 'allauth.socialaccount.providers.soundcloud',
    'allauth.socialaccount.providers.twitter',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.markup',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.comments',
    'django.contrib.markup',
    'innovation',
    'south',
    'myhacks',
]

if not DEBUG:
    INSTALLED_APPS += ['allauth.socialaccount.providers.facebook']

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'js_sdk',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': ('[%(asctime)s] %(levelname)s %(message)s '
                       '(%(filename)s:%(lineno)d).'),
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'innovation': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

SOUTH_MIGRATION_MODULES = {
    'profiles': 'innovation.projectmigrations.profiles',
}


# File Browser
FILEBROWSER_VERSIONS = {
    'fb_thumb': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
    'thumbnail': {'verbose_name': 'Thumbnail (140px)', 'width': 140, 'height': '', 'opts': ''},
    'small': {'verbose_name': 'Small (300px)', 'width': 300, 'height': '', 'opts': ''},
    'medium': {'verbose_name': 'Medium (460px)', 'width': 460, 'height': '', 'opts': ''},
    'big': {'verbose_name': 'Big (620px)', 'width': 620, 'height': '', 'opts': ''},
    'cropped': {'verbose_name': 'Cropped (60x60px)', 'width': 60, 'height': 60, 'opts': 'crop'},
    'croppedthumbnail': {'verbose_name': 'Cropped Thumbnail (140x140px)', 'width': 140, 'height': 140, 'opts': 'crop'},
    'item_banner': {'verbose_name': 'Item Banner', 'width': 550, 'height': 351, 'opts': 'crop upscale'},
}
