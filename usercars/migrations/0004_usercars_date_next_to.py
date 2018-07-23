# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '0003_auto_20151123_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercars',
            name='date_next_to',
            field=models.PositiveIntegerField(default=1, blank=True, choices=[(1, 'one year'), (2, 'two years')]),
        ),
    ]
