# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='notifications',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
