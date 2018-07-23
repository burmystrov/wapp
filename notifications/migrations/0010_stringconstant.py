# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0009_sentnotifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='StringConstant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mileage_reminder', models.TextField(help_text='Text to show in push notification about need of mileage update.')),
                ('mileage_reminder_en', models.TextField(help_text='Text to show in push notification about need of mileage update.', null=True)),
                ('mileage_reminder_ru', models.TextField(help_text='Text to show in push notification about need of mileage update.', null=True)),
                ('maintenance_reminder', models.TextField(help_text='Text to show in push notification about need to visit service center.')),
                ('maintenance_reminder_en', models.TextField(help_text='Text to show in push notification about need to visit service center.', null=True)),
                ('maintenance_reminder_ru', models.TextField(help_text='Text to show in push notification about need to visit service center.', null=True)),
            ],
        ),
    ]
