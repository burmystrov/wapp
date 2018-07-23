# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Guidelines


class GuidelinesSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Guidelines
        fields = ('id', 'name', 'file_video')
