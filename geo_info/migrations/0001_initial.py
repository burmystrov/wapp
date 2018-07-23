# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geoname_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('name_en', models.CharField(max_length=200, null=True, db_index=True)),
                ('name_ru', models.CharField(max_length=200, null=True, db_index=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geoname_id', models.IntegerField(unique=True)),
                ('name', models.CharField(unique=True, max_length=200, db_index=True)),
                ('name_en', models.CharField(max_length=200, unique=True, null=True, db_index=True)),
                ('name_ru', models.CharField(max_length=200, unique=True, null=True, db_index=True)),
                ('code2', models.CharField(unique=True, max_length=2)),
                ('code3', models.CharField(unique=True, max_length=3)),
                ('tld', models.CharField(db_index=True, max_length=5, blank=True)),
                ('continent', models.CharField(db_index=True, max_length=2, choices=[('OC', 'Oceania'), ('EU', 'Europe'), ('AF', 'Africa'), ('NA', 'North America'), ('AN', 'Antarctica'), ('SA', 'South America'), ('AS', 'Asia')])),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geoname_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('name_en', models.CharField(max_length=200, null=True, db_index=True)),
                ('name_ru', models.CharField(max_length=200, null=True, db_index=True)),
                ('geoname_code', models.CharField(max_length=50, db_index=True)),
                ('country', models.ForeignKey(to='geo_info.Country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(to='geo_info.Country'),
        ),
        migrations.AddField(
            model_name='city',
            name='region',
            field=models.ForeignKey(blank=True, to='geo_info.Region', null=True),
        ),
    ]
