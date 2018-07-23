# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import now


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_notifications_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notifications',
            name='date',
            field=models.DateField(default=now().date()),
        ),
    ]
