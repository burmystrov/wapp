# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guidelines', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='guidelines',
            options={'verbose_name': 'Guidelines'},
        ),
        migrations.AddField(
            model_name='guidelines',
            name='file_video_en',
            field=models.FileField(null=True, upload_to='guidelines'),
        ),
        migrations.AddField(
            model_name='guidelines',
            name='file_video_ru',
            field=models.FileField(null=True, upload_to='guidelines'),
        ),
        migrations.AddField(
            model_name='guidelines',
            name='name_en',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AddField(
            model_name='guidelines',
            name='name_ru',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
