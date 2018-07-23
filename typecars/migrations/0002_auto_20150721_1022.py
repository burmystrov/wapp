# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('typecars', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brands',
            options={'ordering': ['-id'], 'verbose_name': 'brand', 'verbose_name_plural': 'brands'},
        ),
        migrations.AlterModelOptions(
            name='models',
            options={'ordering': ['-id'], 'verbose_name': 'model', 'verbose_name_plural': 'models'},
        ),
    ]
