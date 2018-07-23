# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from datetime import datetime, timedelta

import pytz
from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel

from common.utils import month_before, send_notifications
from constance import config


class NotificationOptions(models.Model):
    class Names(object):
        MILEAGE = 'Mileage'
        MAINTENANCE1 = 'Maintenance1'
        MAINTENANCE2 = 'Maintenance2'
        CHOICES = (
            (MILEAGE, _('Mileage')),
            (MAINTENANCE1, _('Maintenance 1')),
            (MAINTENANCE2, _('Maintenance 2')),
        )

    class Periods(object):
        class Mileage(object):
            DAILY = 100
            WEEKLY = 101
            MONTHLY = 102
            THREE_TIMES_PER_WEEK = 103
            TWO_TIMES_PER_MONTH = 104
            ALL = list(range(100, 105))

        class Maintenance(object):
            AT_TIME_OF_SERVICE = 200
            ONE_DAY_BEFORE = 201
            TWO_DAYS_BEFORE = 202
            A_WEEK_BEFORE = 203
            A_14_DAYS_BEFORE = 204
            A_MONTH_BEFORE = 205
            ALL = list(range(200, 206))

            @classmethod
            def shift_date(cls, date_value, period):
                if period == cls.A_MONTH_BEFORE:
                    return month_before(date_value)
                date_mapping = {
                    cls.AT_TIME_OF_SERVICE: timedelta(days=0),
                    cls.ONE_DAY_BEFORE: timedelta(days=1),
                    cls.TWO_DAYS_BEFORE: timedelta(days=2),
                    cls.A_WEEK_BEFORE: timedelta(days=7),
                    cls.A_14_DAYS_BEFORE: timedelta(days=14),
                }

                if period not in date_mapping:
                    return date_value

                return date_value - date_mapping[period]

    DEFAULTS = [
        {
            'name': Names.MILEAGE,
            'period': Periods.Mileage.WEEKLY,
        },
        {
            'name': Names.MAINTENANCE1,
            'period': Periods.Maintenance.A_WEEK_BEFORE,
        },
        {
            'name': Names.MAINTENANCE2,
            'period': Periods.Maintenance.ONE_DAY_BEFORE,
        },
    ]

    LIMITS = {
        Periods.Mileage.DAILY: {
            'days': 0, 'count': 1, 'weekdays': range(7)
        },
        Periods.Mileage.THREE_TIMES_PER_WEEK: {
            'days': 7, 'count': 3, 'weekdays': [0, 2, 4]
        },
        Periods.Mileage.WEEKLY: {
            'days': 7, 'count': 1, 'weekdays': range(7)
        },
        Periods.Mileage.TWO_TIMES_PER_MONTH: {
            'days': 15, 'count': 1, 'weekdays': range(7)
        },
        Periods.Mileage.MONTHLY: {
            'days': 30, 'count': 1, 'weekdays': range(7)
        }
    }

    name = models.CharField(max_length=120, choices=Names.CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    period = models.IntegerField()
    is_active = models.BooleanField(default=False)

    class Meta(object):
        unique_together = ('user', 'name')

    def can_send_push_timezone(self):
        timezone = settings.TIME_ZONE
        if self.user.profile.country and self.user.profile.country.timezone:
            timezone = self.user.profile.country.timezone
        tz = pytz.timezone(timezone)
        hour_now = datetime.now(tz).time().strftime('%H')
        return config.time_push == hour_now

    def can_send_maintenance_reminder(self, date_value):
        if self.name == self.Names.MILEAGE:
            return False
        return self.Periods.Maintenance.shift_date(
            date_value, self.period) == now().date()

    def can_send_mileage_reminder(self, car):
        if self.name == self.Names.MILEAGE:
            limit = self.LIMITS[self.period]

            if now().date().weekday() not in limit['weekdays']:
                return False

            return SentNotifications.objects.filter(
                user_car=car, name=NotificationOptions.Names.MILEAGE,
                created__gte=now().date() - timedelta(days=limit['days'])
            ).count() < limit['count']
        else:
            return False

    @classmethod
    def create_default_notification_options(cls, user):
        for default in cls.DEFAULTS:
            cls.objects.create(user=user, **default)


class SentNotifications(TimeStampedModel):
    name = models.CharField(
        max_length=120, choices=NotificationOptions.Names.CHOICES)
    user_car = models.ForeignKey('usercars.UserCars')
    message = models.TextField(blank=True)
    is_send = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.is_send:
            send_notifications(user=self.user_car.user, message=self.message)
            self.is_send = True
        super(SentNotifications, self).save(
            force_insert=False, force_update=False, using=None,
            update_fields=None
        )
