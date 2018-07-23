# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('usersettings', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersettings',
            name='id',
        ),
        migrations.AlterField(
            model_name='usersettings',
            name='user',
            field=models.OneToOneField(related_name='user_settings', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL),
        ),
    ]
