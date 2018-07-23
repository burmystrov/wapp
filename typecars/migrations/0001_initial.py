# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brands',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(unique=True, max_length=128, verbose_name='brand')),
                ('name_en', models.CharField(max_length=128, unique=True, null=True, verbose_name='brand')),
                ('name_ru', models.CharField(max_length=128, unique=True, null=True, verbose_name='brand')),
                ('image', models.ImageField(upload_to='typecars/brands', verbose_name='image', blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Models',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('name', models.CharField(max_length=128, verbose_name='model')),
                ('name_en', models.CharField(max_length=128, null=True, verbose_name='model')),
                ('name_ru', models.CharField(max_length=128, null=True, verbose_name='model')),
                ('image', models.ImageField(upload_to='typecars/models', verbose_name='image', blank=True)),
                ('service_frequency_mileage', models.IntegerField(verbose_name='service frequency mileage')),
                ('brand', models.ForeignKey(related_name='brand_models', verbose_name='brand', to='typecars.Brands')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='models',
            unique_together=set([('brand', 'name')]),
        ),
    ]
