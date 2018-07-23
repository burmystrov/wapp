# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consumables', '0002_auto_20150818_1223'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumables',
            name='description',
            field=models.TextField(verbose_name='description', blank=True),
        ),
    ]
