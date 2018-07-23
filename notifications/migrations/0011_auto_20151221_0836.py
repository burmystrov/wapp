# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0010_stringconstant'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='user_car',
        ),
        migrations.DeleteModel(
            name='Notifications',
        ),
    ]
