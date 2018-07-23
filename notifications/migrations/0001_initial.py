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
            name='NotificationOptions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120, choices=[('Mileage', 'Mileage'), ('Maintenance1', 'Maintenance 1'), ('Maintenance2', 'Maintenance 2')])),
                ('period', models.IntegerField()),
                ('last_push', models.DateField()),
                ('is_active', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='notificationoptions',
            unique_together=set([('user', 'name')]),
        ),
    ]
