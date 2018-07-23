# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_auto_20151019_1427'),
    ]

    operations = [
        migrations.RenameField(
            model_name='notifications',
            old_name='is_active',
            new_name='active',
        ),
    ]
