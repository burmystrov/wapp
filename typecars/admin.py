# encoding: utf-8
from __future__ import unicode_literals

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from common.mixin.admin import TranslateMediaMixin

from .models import Brands, Models


class BModelAdmin(TranslateMediaMixin, TranslationAdmin):
    list_display = ('id', 'name', 'is_active')
    search_fields = ('=id', 'name')
    list_filter = ('is_active',)

admin.site.register(Brands, BModelAdmin)
admin.site.register(Models, BModelAdmin)
