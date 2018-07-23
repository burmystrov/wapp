# encoding: utf-8
from __future__ import unicode_literals

from django.contrib import admin

from .models import NotificationOptions, SentNotifications


class SentNotificationsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'user_car', 'message', 'is_send'
    )


class NotificationOptionsAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'user', 'period', 'is_active'
    )


admin.site.register(SentNotifications, SentNotificationsAdmin)
admin.site.register(NotificationOptions, NotificationOptionsAdmin)
