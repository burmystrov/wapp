# encoding: utf-8
from __future__ import unicode_literals

import six
from rest_framework import serializers
from common.utils import date_to_timestamp, date_now
from constans import NAME_NOTIFICATIONS
from notifications.params import ParamsForNextMaintenances

from usersettings.models import UserSettings


class AdminSerializer(serializers.ModelSerializer):
    """Adds extra field count for superuser"""
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        return obj.count


class TimeFieldAutoformatSerializerMixin(object):
    """
    Mixin dynamically adds format string in every TimeField depending on time
    format from request object.
    """
    def get_fields(self):
        """
        To minimize overhead by adding format, processing performed in time of
        first access to serializer fields.
        """
        fields = super(
            TimeFieldAutoformatSerializerMixin, self).get_fields()
        #: Modify format string for time fields.
        for field_name, field in six.iteritems(fields):
            if isinstance(field, serializers.TimeField):
                field.format = UserSettings.TimeFormat.get_format_str(
                    self.context['request'].TIME_FORMAT)
        return fields


class ValidationMixin(object):
    def validate_related_field(self, message, attrs, source):
        request = self.context['request']
        related_field = attrs[source]
        if 'is_general' not in related_field.__dict__:
            related_field.is_general = None
        if not related_field.user == request.user and not \
                related_field.is_general:
            raise serializers.ValidationError({source: message})


class UserCarsMixinSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        """Updates `mileage_update` field if there're any changes in comparison
        to previous value.
        """

        if instance.current_mileage != validated_data.get('current_mileage'):
            instance.mileage_update = date_now()
        return super(UserCarsMixinSerializer, self).update(
            instance, validated_data
        )


class NotificationMixinSerializer(object):
    def get_object_car(self, obj):
        try:
            return obj.user_car
        except AttributeError:
            return obj

    def get_notifications(self, obj):
        ntf = ParamsForNextMaintenances(self.get_object_car(obj))
        data = {
            'timestamp': date_to_timestamp(
                ntf.optimum_maintenance_event_date()),
            'name': NAME_NOTIFICATIONS.get(0)
        }
        return data
