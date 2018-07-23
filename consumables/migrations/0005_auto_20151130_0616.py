# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consumables', '0004_auto_20151020_0831'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='consumablescategories',
            unique_together=set([('name', 'user')]),
        ),
    ]
