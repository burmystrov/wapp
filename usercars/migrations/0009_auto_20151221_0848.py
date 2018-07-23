# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '0008_auto_20151221_0847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercars',
            name='last_service_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 21, 8, 48, 17, 653958, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usercars',
            name='last_service_mileage',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
