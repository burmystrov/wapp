# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from push_notifications.api.rest_framework import (APNSDeviceSerializer,
                                                   HexIntegerField)
from push_notifications.models import APNSDevice, GCMDevice
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from notifications.models import NotificationOptions


class HexField(HexIntegerField):
    """
    Fixes error with trying to evaluate invalid data, which breaks validation
    process and leads to 500 errors.
    """
    default_error_messages = {
        'not hex': _('Not a hex number.')
    }

    def to_internal_value(self, data):
        try:
            int(data, 16)
        except ValueError:
            self.fail('not hex')
        return super(HexField, self).to_internal_value(data)


class DeviceSerializerMixin(serializers.ModelSerializer):
    """
    Stores common meta fields for both GCM and APNs device serializers.
    """
    class Meta:
        fields = ('id', 'registration_id', 'active', 'date_created')
        read_only_fields = ('date_created', )


class RegisterGCMDeviceSerializer(serializers.ModelSerializer):
    class Meta(DeviceSerializerMixin.Meta):
        model = GCMDevice
        extra_kwargs = {
            'registration_id': {
                'validators': [
                    UniqueValidator(queryset=GCMDevice.objects.all())
                ]
            }
        }


class RegisterAPNSDeviceSerializer(APNSDeviceSerializer):
    class Meta(DeviceSerializerMixin.Meta):
        model = APNSDevice


class NotificationOptionsSerializer(serializers.ModelSerializer):
    def validate_period(self, value):
        self.instance.period = value
        self.instance.clean()
        return value

    class Meta(object):
        model = NotificationOptions
        fields = ('id', 'name', 'period', 'is_active', )
        read_only_fields = ('name', )
