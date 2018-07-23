# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0002_auto_20160119_1112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchases',
            name='transaction_id',
        ),
        migrations.AddField(
            model_name='purchases',
            name='transaction_base64',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
