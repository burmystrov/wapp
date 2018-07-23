# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('consumables', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumables',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False),
        ),
        migrations.AlterField(
            model_name='consumables',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False),
        ),
    ]
