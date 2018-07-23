# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('consumables', '0005_auto_20151130_0616'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='consumablescategories',
            unique_together=set([]),
        ),
    ]
