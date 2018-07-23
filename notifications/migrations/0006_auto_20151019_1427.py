# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0005_auto_20151019_1032'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notifications',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='notifications',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
