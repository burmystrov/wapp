# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('typecars', '0004_auto_20150803_0919'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brands',
            options={'ordering': ('-id',), 'verbose_name': 'Brand', 'verbose_name_plural': 'Brands'},
        ),
        migrations.AlterField(
            model_name='brands',
            name='image',
            field=models.ImageField(upload_to='type_cars/brands', blank=True),
        ),
        migrations.AlterField(
            model_name='brands',
            name='name',
            field=models.CharField(unique=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='brands',
            name='name_en',
            field=models.CharField(max_length=128, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='brands',
            name='name_ru',
            field=models.CharField(max_length=128, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='models',
            name='image',
            field=models.ImageField(upload_to='type_cars/models', blank=True),
        ),
    ]
