# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0003_auto_20160122_1346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchases',
            old_name='transaction_base64',
            new_name='receipt_data',
        ),
    ]
