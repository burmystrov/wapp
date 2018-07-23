# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('typecars', '0005_auto_20150818_0844'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationImages',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('lat', models.DecimalField(null=True, max_digits=10, decimal_places=6, blank=True)),
                ('long', models.DecimalField(null=True, max_digits=10, decimal_places=6, blank=True)),
                ('name', models.CharField(max_length=128)),
                ('image', models.ImageField(upload_to='location_images/%Y/%m/%d')),
                ('is_main', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='UserCars',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('model_year', models.CharField(max_length=4, verbose_name='year of manufacture')),
                ('current_mileage', models.PositiveIntegerField()),
                ('last_service', models.DateField()),
                ('frequency_run', models.PositiveIntegerField(null=True, choices=[(5, '5.000 km'), (10, '10.000 km'), (15, '15.000 km'), (20, '20.000 km'), (25, '25.000 km')])),
                ('date_next_to', models.DateField(null=True)),
                ('mileage_update', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('model', models.ForeignKey(related_name='model_cars', to='typecars.Models')),
                ('user', models.ForeignKey(related_name='user_cars', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
            },
        ),
        migrations.AddField(
            model_name='locationimages',
            name='user_car',
            field=models.ForeignKey(related_name='car_images', to='usercars.UserCars'),
        ),
    ]
