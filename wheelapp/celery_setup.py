# ~*~ encoding: ~*~
import os

from celery import Celery
from django.conf import settings

#: Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wheelapp.settings')

#: See: http://docs.celeryproject.org/en/latest/userguide/application.html#main-name
app = Celery('wheelapp')
#: Using a string here means the worker will not have to pickle the object when
#: using Windows.
#: See: http://docs.celeryproject.org/en/latest/userguide/application.html#config-from-object
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
