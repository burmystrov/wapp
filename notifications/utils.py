# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.timezone import now

from constance import config

from .models import NotificationOptions, SentNotifications
from .params import ParamsForNextMaintenances


def send_push_notification(car):
    nm = ParamsForNextMaintenances(car)
    date_nmt = nm.optimum_maintenance_event_date()
    ntm = NotificationOptions.objects.filter(
        user=car.user, is_active=True).exclude(
        name=NotificationOptions.Names.MILEAGE)
    for nm in ntm:
        if nm.can_send_maintenance_reminder(date_nmt) \
                and nm.can_send_push_timezone():
            text = config.notification_maintenances_en \
                if car.user.user_settings.lang == 'en' \
                else config.notification_maintenances_ru
            text = text.format((date_nmt - now().date()).days)
            SentNotifications.objects.create(
                name=nm.name, user_car=car, message=text
            )
    nt_mil = NotificationOptions.objects.filter(
        user=car.user, is_active=True,
        name=NotificationOptions.Names.MILEAGE
    )
    for nm in nt_mil:
        if nm.can_send_mileage_reminder(car) and nm.can_send_push_timezone():
            text = config.notification_mileage_en \
                if car.user.user_settings.lang == 'en' \
                else config.notification_mileage_ru
            SentNotifications.objects.create(
                name=nm.name, user_car=car, message=text
            )
