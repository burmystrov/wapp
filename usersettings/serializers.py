# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from rest_framework import serializers

from .models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = UserSettings
        fields = ('lang', 'date_format')
