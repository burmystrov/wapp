# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenances', '0006_maintenances_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maintenances',
            name='timestamp',
        ),
    ]
