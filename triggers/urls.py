# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from django.conf.urls import url

from .views import OpenAppView

urlpatterns = [
    url(r'^open-app$', OpenAppView.as_view(), name='open_app_trigger'),
]
