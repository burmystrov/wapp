# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('typecars', '0002_auto_20150721_1022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='models',
            options={'ordering': ['-id'], 'verbose_name': 'Model', 'verbose_name_plural': 'Models'},
        ),
        migrations.AlterField(
            model_name='models',
            name='brand',
            field=models.ForeignKey(related_name='brand_models', to='typecars.Brands'),
        ),
        migrations.AlterField(
            model_name='models',
            name='service_frequency_mileage',
            field=models.IntegerField(),
        ),
    ]
