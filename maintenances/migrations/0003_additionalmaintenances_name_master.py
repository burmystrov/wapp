# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenances', '0002_auto_20150819_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='additionalmaintenances',
            name='name_master',
            field=models.TextField(verbose_name='name', blank=True),
        ),
    ]
