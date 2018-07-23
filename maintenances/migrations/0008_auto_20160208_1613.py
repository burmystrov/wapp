# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenances', '0007_remove_maintenances_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maintenances',
            name='datetime',
            field=models.DateTimeField(null=True, verbose_name='datetime', blank=True),
        ),
    ]
