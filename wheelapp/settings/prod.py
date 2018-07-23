# encoding: utf-8
from __future__ import unicode_literals

from .base import *

ALLOWED_HOSTS = ['wheelapp.mightypuppy.com']

# MANAGER CONFIGURATION
# https://docs.djangoproject.com/en/1.8/ref/settings/#admins
ADMINS = (
    ('Your Name', 'your_email@example.com'),
)


# EMAIL CONFIGURATION
# https://docs.djangoproject.com/en/1.8/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# https://docs.djangoproject.com/en/1.8/ref/settings/#email-host
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')

# https://docs.djangoproject.com/en/1.8/ref/settings/#email-host-user
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')

# https://docs.djangoproject.com/en/1.8/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')

# https://docs.djangoproject.com/en/1.8/ref/settings/#email-port
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)

EMAIL_USE_TLS = True

# https://docs.djangoproject.com/en/1.8/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER

DEFAULT_FROM_EMAIL = EMAIL_ADDRESS_FROM = os.environ.get('EMAIL_ADDRESS_FROM')
