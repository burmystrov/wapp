# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_format', models.SmallIntegerField(default=24, verbose_name='Time format', choices=[(12, '12 hour format'), (24, '24 hour format')])),
                ('lang', models.CharField(default='en', max_length=2, verbose_name='Language code', choices=[('en', 'English'), ('ru', 'Russian')])),
                ('user', models.OneToOneField(related_name='user_settings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User settings',
            },
        ),
    ]
