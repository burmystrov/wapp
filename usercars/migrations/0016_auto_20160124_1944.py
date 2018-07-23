# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '0015_auto_20160124_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercars',
            name='next_maintenances_new',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='usercars',
            name='next_maintenances_old',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
