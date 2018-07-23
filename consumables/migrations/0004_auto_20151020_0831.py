# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consumables', '0003_consumables_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consumables',
            name='image',
            field=models.ImageField(upload_to='consumables/images', verbose_name='image', blank=True),
        ),
    ]
