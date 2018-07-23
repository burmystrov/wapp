# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0011_auto_20151221_0836'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StringConstant',
        ),
        migrations.AddField(
            model_name='sentnotifications',
            name='is_send',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sentnotifications',
            name='message',
            field=models.TextField(blank=True),
        ),
    ]
