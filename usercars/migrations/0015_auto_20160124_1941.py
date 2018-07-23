# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '0014_auto_20151222_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercars',
            name='next_maintenances_new',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=20, blank=True),
        ),
        migrations.AddField(
            model_name='usercars',
            name='next_maintenances_old',
            field=models.DecimalField(null=True, max_digits=20, decimal_places=20, blank=True),
        ),
    ]
