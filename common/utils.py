# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

import datetime

from django.utils.timezone import now
from push_notifications.models import APNSDevice, GCMDevice


def to_int(num, ret=0):
    try:
        return int(num)
    except ValueError:
        return ret


def month_before(date_value):
    """
    Returns date minus one month.

    :param datetime.date date_value: Date to transform.
    :rtype: datetime.date
    """
    year, month = date_value.year, date_value.month
    # Year contains number of months minus one.
    # Months are zero based now, so we make minus two.
    year *= 12 + month - 2
    # Retrieve month starting from one.
    month = year % 12 + 1
    # Use integer division to retrieve number of full years.
    year /= 12
    return datetime.date(year, month, date_value.day)


def date_to_timestamp(d):
    if d and isinstance(d, datetime.date):
        epoch = datetime.date(1970, 1, 1)
        timestamp = (d - epoch).total_seconds()
        return timestamp
    else:
        return None


def datetime_to_timestamp(dt):
    if dt and isinstance(dt, datetime.datetime):
        epoch = datetime.datetime(1970, 1, 1, 0, 0, 0)
        timestamp = (dt.replace(tzinfo=None) - epoch).total_seconds()
        return timestamp
    else:
        return None


def date_now():
    return now()


def send_notifications(user, message=None, extra=False):
    # gcm = GCMDevice.objects.filter(user=user, active=True)
    apns = APNSDevice.objects.filter(user=user, active=True)
    if extra:
        # gcm.send_message(message, extra)
        apns.send_message(message, extra=extra)
    else:
        # gcm.send_message(message)
        apns.send_message(message)
