# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('typecars', '0006_auto_20151221_0836'),
    ]

    operations = [
        migrations.AlterField(
            model_name='models',
            name='frequency_run',
            field=models.IntegerField(default=10, blank=True, choices=[(5, '5.000 km'), (10, '10.000 km'), (15, '15.000 km'), (20, '20.000 km'), (25, '25.000 km'), (30, '30.000 km')]),
        ),
    ]
