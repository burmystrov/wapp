# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '0002_auto_20150921_1757'),
        ('notifications', '0002_auto_20151016_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('message', models.TextField()),
                ('user_car', models.ForeignKey(to='usercars.UserCars')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
