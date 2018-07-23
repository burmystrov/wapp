# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usercars', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consumables',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('image', models.ImageField(upload_to='consumables/images', verbose_name='image')),
                ('created', models.DateField(auto_now_add=True, verbose_name='created')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
            ],
            options={
                'verbose_name': 'Consumable',
                'verbose_name_plural': 'Consumables',
            },
        ),
        migrations.CreateModel(
            name='ConsumablesCategories',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('name_en', models.CharField(max_length=128, null=True, verbose_name='name')),
                ('name_ru', models.CharField(max_length=128, null=True, verbose_name='name')),
                ('is_active', models.BooleanField(default=True, verbose_name='active')),
                ('is_general', models.BooleanField(default=False, verbose_name='general')),
                ('user', models.ForeignKey(related_name='user_consumables', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AddField(
            model_name='consumables',
            name='category',
            field=models.ForeignKey(related_name='category_consumables', verbose_name='category', to='consumables.ConsumablesCategories'),
        ),
        migrations.AddField(
            model_name='consumables',
            name='user_car',
            field=models.ForeignKey(related_name='car_consumables', verbose_name='car', to='usercars.UserCars'),
        ),
    ]
