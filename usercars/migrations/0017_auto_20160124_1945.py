# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '0016_auto_20160124_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercars',
            name='next_maintenances_new',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='usercars',
            name='next_maintenances_old',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
