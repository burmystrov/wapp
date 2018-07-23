# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geo_info', '0002_country_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='timezone',
            field=models.CharField(max_length=64, blank=True),
        ),
    ]
