# encoding: utf-8
from __future__ import unicode_literals

from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from common.fields import Base64ImageField
from common.mixin.serializers import (NotificationMixinSerializer,
                                      UserCarsMixinSerializer)
from common.utils import date_now
from usercars.models import LocationImages, UserCars


class UserCarsSerializer(NotificationMixinSerializer, UserCarsMixinSerializer):
    image = serializers.SerializerMethodField()
    model_year = serializers.IntegerField(min_value=1800, max_value=3000)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    notifications = serializers.SerializerMethodField()

    class Meta:
        model = UserCars
        fields = (
            'id', 'user', 'model', 'model_year', 'current_mileage',
            'last_service_date', 'frequency_run', 'date_next_to', 'image',
            'notifications', 'last_service_mileage'
        )
        read_only_fields = ('image',)

    def get_image(self, obj):
        try:
            image = obj.car_images.get(is_main=True)
            data = {
                'id': image.id,
                'url': image.image.url
            }
            return data
        except ObjectDoesNotExist:
            return None

    def validate(self, attrs):
        current_mileage = attrs.get('current_mileage')
        last_service_mileage = attrs.get('last_service_mileage')
        last_service_date = attrs.get('last_service_date')
        date_next_to = attrs.get('date_next_to')
        frequency_run = attrs.get('frequency_run')

        if ((last_service_mileage and last_service_date is None) or
                (last_service_date and last_service_mileage is None)):
            raise serializers.ValidationError(_(
                'last_service_mileage and last_service_date - these two '
                'fields are either required or they can be empty'))

        if last_service_mileage > current_mileage:
            raise serializers.ValidationError(_(
                'Current car mileage cannot be less than car '
                'mileage of the last maintenance'))

        if last_service_date and last_service_date > now().date():
            raise serializers.ValidationError(_(
                'Date of the last maintenance cannot be bigger '
                'than current date'))

        if not last_service_mileage:
            attrs.update(
                {
                    'last_service_mileage': current_mileage,
                    'last_service_date': date_now().date()
                }
            )
        if not date_next_to:
            attrs.update(
                {'date_next_to': UserCars.DateFrequencies.ONE_YEAR}
            )
        if not frequency_run:
            attrs.update(
                {
                    'frequency_run': attrs.get('model').frequency_run
                    if attrs.get('model') else UserCars.MileageFrequencies.TEN
                }
            )

        return attrs


class CarMileageSerializer(NotificationMixinSerializer,
                           UserCarsMixinSerializer):
    notifications = serializers.SerializerMethodField()

    class Meta:
        model = UserCars
        fields = ('id', 'current_mileage', 'notifications')


class LocationImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    def validate(self, attrs):
        lat = attrs.get('lat')
        lng = attrs.get('long')
        if lat or lng:
            if not (lat and lng):
                raise serializers.ValidationError(
                    _('long and lat attributes must be provided together.')
                )
        return attrs

    def validate_user_car(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError(
                _('You can only add image to your car')
            )
        return value

    class Meta:
        model = LocationImages
        fields = ('id', 'name', 'image', 'user_car', 'lat', 'long', 'is_main')


class UpdateLocationImageSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = LocationImages
        fields = ('id', 'name', 'image', 'user_car', 'lat', 'long', 'is_main')
        read_only_fields = ('user_car', 'lat', 'long')
