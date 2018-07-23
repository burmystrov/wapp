# encoding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from .models import City, Country

admin.site.register(Country)
admin.site.register(City)
