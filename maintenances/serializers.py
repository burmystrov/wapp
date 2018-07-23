# encoding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from common.mixin.serializers import (NotificationMixinSerializer,
                                      TimeFieldAutoformatSerializerMixin,
                                      ValidationMixin)
from common.utils import datetime_to_timestamp

from .models import AdditionalMaintenances, Maintenances


class MaintenancesSerializer(NotificationMixinSerializer,
                             TimeFieldAutoformatSerializerMixin,
                             ValidationMixin,
                             serializers.ModelSerializer):
    maintenances_timestamp = serializers.SerializerMethodField()
    notifications = serializers.SerializerMethodField()

    class Meta(object):
        model = Maintenances
        fields = (
            'id', 'user_car', 'name', 'datetime', 'mileage_to', 'type',
            'description', 'maintenances_timestamp', 'notifications'
        )

    def validate(self, attrs):
        massage = _('Current user has no access to this car')
        self.validate_related_field(massage, attrs, 'user_car')
        return attrs

    def get_maintenances_timestamp(self, obj):
        return datetime_to_timestamp(obj.datetime)


class AdditionalMaintenancesSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = AdditionalMaintenances
        fields = ('am', 'phone_master', 'name_master', 'description',
                  'lat', 'lon')
        read_only_fields = ('am',)
