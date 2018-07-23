# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('typecars', '0003_auto_20150723_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brands',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='models',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
