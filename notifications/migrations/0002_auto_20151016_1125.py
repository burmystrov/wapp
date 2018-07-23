# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationoptions',
            name='last_push',
            field=models.DateField(null=True),
        ),
    ]
