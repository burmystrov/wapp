# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('typecars', '0005_auto_20150818_0844'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='models',
            name='service_frequency_mileage',
        ),
        migrations.AddField(
            model_name='models',
            name='frequency_run',
            field=models.PositiveIntegerField(default=10, blank=True, choices=[(5, '5.000 km'), (10, '10.000 km'), (15, '15.000 km'), (20, '20.000 km'), (25, '25.000 km'), (30, '30.000 km')]),
        ),
    ]
