# encoding: utf-8
from __future__ import unicode_literals

import os
from sys import path

from django.utils.translation import ugettext_lazy as _

from celery.schedules import crontab


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)
CACHE_DIR = os.path.join(BASE_DIR, 'cache')

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(ROOT_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'm1o3e89a975xlnxwt+i$f97zjp=f_u+c_%5&@1pb68jj_iz0b7')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Application definition
DJANGO_APPS = (
    'modeltranslation',  # 3rd party app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'push_notifications',
    'constance',
    'constance.backends.database',
)

LOCAL_APPS = (
    'accounts',
    'statistics',
    'geo_info',
    'typecars',
    'usercars',
    'consumables',
    'maintenances',
    'usersettings',
    'guidelines',
    'notifications',
    'purchase',
    'triggers',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'usersettings.middleware.UserDefinedLocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'wheelapp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(BASE_DIR, 'templates'),),
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'wheelapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('db_name', 'wheelapp'),
        'USER': os.environ.get('db_user', 'wheelapp'),
        'PASSWORD': os.environ.get('db_pwd', 'wheelapp'),
        'HOST': os.environ.get('db_host', 'localhost'),
        'PORT': os.environ.get('db_port', ''),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

DEFAULT_LANGUAGE = 'en'

MODELTRANSLATION_DEFAULT_LANGUAGE = DEFAULT_LANGUAGE
MODELTRANSLATION_TRANSLATION_FILES = [
    'geo_info.translation',
]
#: NOTE: change this carefully, as many models are dependent on it
MODELTRANSLATION_LANGUAGES = ['en', 'ru']
MODELTRANSLATION_ENABLE_FALLBACKS = True
MODELTRANSLATION_FALLBACK_LANGUAGES = ('en', 'ru')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# https://docs.djangoproject.com/en/1.8/ref/settings/#static-root
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# MEDIA CONFIGURATION
# https://docs.djangoproject.com/en/1.8/ref/settings/#media-root
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# https://docs.djangoproject.com/en/1.8/ref/settings/#media-url
MEDIA_URL = '/media/'

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

AUTH_USER_MODEL = 'accounts.User'

SOCIAL_PROVIDERS = ['google', 'facebook']
OAUTH = {
    'facebook': {
        'client_id': os.environ.get('facebook_client_id'),
        'client_secret': os.environ.get('facebook_client_secret')
    },
    'google': {
        'client_id': os.environ.get('google_client_id'),
        'client_secret': os.environ.get('google_client_secret')

    }
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_filters.backends.DjangoFilterBackend',
    ),
    'PAGE_SIZE': 20,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json'
}

# User cars
USER_CARS_FREE = 1
USER_CARS_PAID = 5
# Amount of images to be added to user car
USER_IMAGES_FREE = 1
USER_IMAGES_PAID = 5

# Geo info
GEO_INFO_CACHE = os.path.join(CACHE_DIR, 'geo_info')
GEO_INFO_STORAGE = os.environ.get('GEO_INFO_STORAGE', '')

COUNTRY_SOURCES = ['{}countryInfo.txt'.format(GEO_INFO_STORAGE)]
REGION_SOURCES = ['{}admin1CodesASCII.txt'.format(GEO_INFO_STORAGE)]
CITY_SOURCES = ['{}cities15000.zip'.format(GEO_INFO_STORAGE)]
TRANSLATION_SOURCES = ['{}alternateNames.zip'.format(GEO_INFO_STORAGE)]


# CELERY CONFIG
# See: http://docs.celeryproject.org/en/latest/configuration.html#broker-url
BROKER_URL = 'amqp://'
# See: http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html#crontab-schedules
CELERYBEAT_SCHEDULE = {
    # Executes every day at 10:00 A.M
    'send-push-notification-reminder': {
        'task': 'notifications.tasks.send_push_notifications',
        'schedule': crontab(hour=1),
    },
}
# END CELERY CONFIG


# DJANGO PUSH NOTIFICATIONS
# See: https://github.com/jleclanche/django-push-notifications/blob/1.3.1/README.rst#settings-list
PUSH_NOTIFICATIONS_SETTINGS = {
    'GCM_API_KEY': os.environ.get('gcm_api_key'),
    'APNS_CERTIFICATE': os.environ.get('apns_certificate_path'),
}
# END DJANGO PUSH NOTIFICATIONS

# CONSTANCE settings
CONSTANCE_CONFIG = {
    'time_push': ('09', 'hours (format XX)'),
    'notification_mileage_ru': (
        'Текст уведомления об пробеге', 'text for mileage notification(ru)'),
    'notification_mileage_en': (
        'Test mileage notification', 'text for mileage notification(en)'),
    'notification_maintenances_en': (
        'WheelApp: in {} days you assumably have a next servicing event',
        'text for maintenances notification(en)'),
    'notification_maintenances_ru': (
        'WheelApp: in {} days you assumably have a next servicing event',
        'text for maintenances notification(ru)'),
}
CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

ITUNES_PASSWORD = os.environ.get('itunes_password')


REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER':
        'common.serializers.PasswordResetHtmlSerializer'
}
