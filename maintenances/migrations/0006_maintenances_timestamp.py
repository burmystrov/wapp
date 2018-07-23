# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenances', '0005_auto_20160121_0937'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenances',
            name='timestamp',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
