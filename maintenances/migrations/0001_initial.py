# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usercars', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalMaintenances',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone_master', models.CharField(max_length=128, verbose_name='phone')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('lat', models.DecimalField(null=True, max_digits=10, decimal_places=6, blank=True)),
                ('lon', models.DecimalField(null=True, max_digits=10, decimal_places=6, blank=True)),
            ],
            options={
                'verbose_name': 'Additional',
                'verbose_name_plural': 'Additionals',
            },
        ),
        migrations.CreateModel(
            name='Maintenances',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('date', models.DateField(verbose_name='date')),
                ('time', models.TimeField(verbose_name='time')),
                ('mileage_am', models.PositiveIntegerField(verbose_name='mileage')),
                ('type', models.CharField(max_length=15, verbose_name='type', choices=[('Scheduled', 'Scheduled'), ('Unplanned', 'Unplanned')])),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('user_car', models.ForeignKey(related_name='car_maintenances', verbose_name='car', to='usercars.UserCars')),
            ],
            options={
                'verbose_name': 'Maintenance',
                'verbose_name_plural': 'Maintenances',
            },
        ),
        migrations.AddField(
            model_name='additionalmaintenances',
            name='am',
            field=models.OneToOneField(related_name='maintenance_additional', verbose_name='maintenance', to='maintenances.Maintenances'),
        ),
    ]
