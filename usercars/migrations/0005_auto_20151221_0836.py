# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '0004_usercars_date_next_to'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercars',
            name='last_service',
        ),
        migrations.AddField(
            model_name='usercars',
            name='last_service_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 21, 8, 36, 31, 248505, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='usercars',
            name='last_service_mileage',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
