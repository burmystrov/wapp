# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '0002_auto_20150921_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercars',
            name='date_next_to',
        ),
        migrations.AlterField(
            model_name='usercars',
            name='frequency_run',
            field=models.PositiveIntegerField(default=20, blank=True, choices=[(5, '5.000 km'), (10, '10.000 km'), (15, '15.000 km'), (20, '20.000 km'), (25, '25.000 km'), (30, '30.000 km')]),
        ),
    ]
