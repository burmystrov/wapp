# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '0007_auto_20151221_0845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercars',
            name='last_service_date',
            field=models.DateField(default=datetime.datetime(2015, 12, 21, 8, 47, 29, 88998, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='usercars',
            name='last_service_mileage',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
