# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('maintenances', '0008_auto_20160208_1613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenances',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 16, 9, 20, 35, 244880, tzinfo=utc), verbose_name='datetime'),
            preserve_default=False,
        ),
    ]
