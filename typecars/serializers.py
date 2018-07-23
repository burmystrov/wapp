# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import serializers

from common.mixin.serializers import AdminSerializer

from .models import Brands, Models


class AdminBrandSerializer(AdminSerializer):
    class Meta:
        model = Brands
        fields = ('id', 'name', 'image', 'count')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brands
        fields = ('id', 'name', 'image')


class AdminModelSerializer(AdminSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Models
        fields = ('id', 'brand', 'name', 'image', 'count')


class ModelSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Models
        fields = ('id', 'brand', 'name', 'image')
