# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '0004_usercars_date_next_to'),
        ('notifications', '0008_auto_20151021_0726'),
    ]

    operations = [
        migrations.CreateModel(
            name='SentNotifications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=120, choices=[('Mileage', 'Mileage'), ('Maintenance1', 'Maintenance 1'), ('Maintenance2', 'Maintenance 2')])),
                ('user_car', models.ForeignKey(to='usercars.UserCars')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
