# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20150717_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oauthaccount',
            name='provider',
            field=models.CharField(max_length=15, choices=[('facebook', 'Facebook'), ('google', 'Google')]),
        ),
    ]
