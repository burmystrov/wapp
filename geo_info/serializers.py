# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from common.mixin.serializers import AdminSerializer

from .models import City, Country


class AdminCountrySerializer(AdminSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'count')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')


class AdminCitySerializer(AdminSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'country', 'count')


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'country')
