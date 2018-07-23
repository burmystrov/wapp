# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenances', '0004_auto_20160120_1046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additionalmaintenances',
            name='id',
        ),
        migrations.AlterField(
            model_name='additionalmaintenances',
            name='am',
            field=models.OneToOneField(related_name='maintenance_additional', primary_key=True, serialize=False, to='maintenances.Maintenances', verbose_name='maintenance'),
        ),
    ]
