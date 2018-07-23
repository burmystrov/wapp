# encoding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from .models import AdditionalMaintenances, Maintenances


class MaintenancesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'user_car', 'datetime', 'type', 'mileage_to')
    search_fields = ('=id', 'name')
    list_filter = ('type',)


class AdditionalMaintenancesAdmin(admin.ModelAdmin):
    list_display = (
        'am', 'phone_master', 'description', 'lat', 'lon')
    search_fields = ('=am', 'name')


admin.site.register(Maintenances, MaintenancesAdmin)
admin.site.register(AdditionalMaintenances, AdditionalMaintenancesAdmin)
