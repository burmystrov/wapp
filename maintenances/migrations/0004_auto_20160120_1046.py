# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('maintenances', '0003_additionalmaintenances_name_master'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenances',
            name='date',
        ),
        migrations.RemoveField(
            model_name='maintenances',
            name='time',
        ),
        migrations.AddField(
            model_name='maintenances',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 20, 10, 46, 16, 513180, tzinfo=utc), verbose_name='datetime'),
            preserve_default=False,
        ),
    ]
