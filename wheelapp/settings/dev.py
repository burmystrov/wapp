# encoding: utf-8
from __future__ import unicode_literals
from .base import *

# DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# TOOLBAR CONFIGURATION
# See: http://django-debug-toolbar.readthedocs.org/en/latest/installation.html#explicit-setup
INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_PATCH_SETTINGS = False
# http://django-debug-toolbar.readthedocs.org/en/latest/installation.html
INTERNAL_IPS = ('127.0.0.1',)
# Allow debug toolbar for all requests.
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True,
}

# EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
