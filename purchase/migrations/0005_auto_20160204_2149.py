# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0004_auto_20160124_0759'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchases',
            name='response',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='purchases',
            name='transaction_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 2, 4, 21, 49, 41, 228895, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchases',
            name='transaction_id',
            field=models.CharField(default=datetime.datetime(2016, 2, 4, 21, 49, 43, 723165, tzinfo=utc), max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='purchases',
            name='transaction_state',
            field=models.CharField(default=datetime.datetime(2016, 2, 4, 21, 49, 46, 547148, tzinfo=utc), max_length=128),
            preserve_default=False,
        ),
    ]
