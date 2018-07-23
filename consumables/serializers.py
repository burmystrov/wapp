# encoding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from common.fields import Base64ImageField
from common.mixin.serializers import ValidationMixin
from consumables.models import Consumables, ConsumablesCategories


class AdminConsumablesCategoriesSerializer(serializers.ModelSerializer):

    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        try:
            return obj.count
        except AttributeError:
            return 0

    class Meta:
        model = ConsumablesCategories
        read_only_fields = ('is_general', 'count')
        fields = ('id', 'name_en', 'name_ru', 'is_general', 'count')


class ConsumablesCategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsumablesCategories
        read_only_fields = ('is_general', )
        fields = ('id', 'name', 'is_general')


class ConsumablesSerializer(ValidationMixin, serializers.ModelSerializer):
    image = Base64ImageField(required=False, allow_null=True)

    def validate(self, attrs):
        massage_dict = {
            'category': _('Current user has no access to this category'),
            'user_car': _('Current user has no access to this car')
        }
        for source in massage_dict.keys():
            self.validate_related_field(massage_dict[source], attrs, source)
        return attrs

    class Meta:
        model = Consumables
        read_only_fields = ('created',)
        fields = (
            'id', 'name', 'description', 'category', 'user_car', 'image',
            'created',
        )
