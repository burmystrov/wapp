# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0007_auto_20151019_1430'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notifications',
            options={},
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='active',
        ),
    ]
