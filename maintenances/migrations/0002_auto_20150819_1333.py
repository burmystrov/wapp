# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenances', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='maintenances',
            old_name='mileage_am',
            new_name='mileage_to',
        ),
    ]
