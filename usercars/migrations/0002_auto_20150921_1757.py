# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercars',
            name='frequency_run',
            field=models.PositiveIntegerField(null=True, choices=[(5, '5.000 km'), (10, '10.000 km'), (15, '15.000 km'), (20, '20.000 km'), (25, '25.000 km'), (30, '30.000 km')]),
        ),
    ]
