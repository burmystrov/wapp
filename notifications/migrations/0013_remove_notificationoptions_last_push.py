# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0012_auto_20151222_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationoptions',
            name='last_push',
        ),
    ]
