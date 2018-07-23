# encoding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from .models import Purchases


class PurchasesAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'is_check'
    )


admin.site.register(Purchases, PurchasesAdmin)
