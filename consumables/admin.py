# encoding: utf-8
from __future__ import unicode_literals

from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from common.mixin.admin import TranslateMediaMixin

from .models import Consumables, ConsumablesCategories


class ConsumablesCategoriesAdmin(TranslateMediaMixin, TranslationAdmin):
    list_display = ('id', 'name', 'user', 'is_active', 'is_general')
    search_fields = ('=id', 'name')
    list_filter = ('is_active', 'is_general')


class ConsumablesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'category', 'user_car', 'created', 'is_active')
    search_fields = ('=id', 'name')
    list_filter = ('is_active',)


admin.site.register(ConsumablesCategories, ConsumablesCategoriesAdmin)
admin.site.register(Consumables, ConsumablesAdmin)
