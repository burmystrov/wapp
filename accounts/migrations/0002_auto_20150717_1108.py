# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('provider', models.CharField(max_length=15, choices=[('fb', 'Facebook'), ('google', 'Google')])),
                ('uid', models.CharField(max_length=255)),
                ('user', models.ForeignKey(related_name='social_accounts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.ForeignKey(related_name='user_cities', blank=True, to='geo_info.City', null=True),
        ),
        migrations.AlterUniqueTogether(
            name='oauthaccount',
            unique_together=set([('provider', 'uid')]),
        ),
    ]
