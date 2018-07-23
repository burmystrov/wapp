# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '0006_auto_20151221_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercars',
            name='date_next_to',
            field=models.IntegerField(default=1, blank=True, choices=[(1, 'one year'), (2, 'two years')]),
        ),
        migrations.AlterField(
            model_name='usercars',
            name='frequency_run',
            field=models.IntegerField(default=20, blank=True, choices=[(5, '5.000 km'), (10, '10.000 km'), (15, '15.000 km'), (20, '20.000 km'), (25, '25.000 km'), (30, '30.000 km')]),
        ),
        migrations.AlterField(
            model_name='usercars',
            name='last_service_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 21, 8, 45, 50, 135418, tzinfo=utc)),
        ),
    ]
