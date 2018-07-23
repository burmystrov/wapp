# encoding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from accounts.providers.base import (ProviderException,
                                     RequiredFieldsException,
                                     UnableRetrieveRequiredData)
from accounts.proxies import SignUpModelProxy
from geo_info.models import City

from .fields import SexField
from .models import Profile, User
from .providers import registry


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'is_paid', 'email')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    sex = SexField()
    image = serializers.ImageField(required=False, allow_null=True)
    location = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            'user', 'sex', 'city', 'date_birth', 'image', 'lat', 'long',
            'fullname', 'location'
        )

    def get_location(self, obj):
        if obj.city:
            data = {
                'city': {
                    'id': obj.city_id,
                    'name': obj.city.name
                },
                'country': {
                    'id': obj.city.country_id,
                    'name': obj.city.country.name
                }
            }
            return data


class SignUpSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=30, min_length=1)
    fullname = serializers.CharField(max_length=128, min_length=1)
    email = serializers.EmailField()
    sex = SexField()
    password = serializers.CharField(max_length=128, write_only=True)
    password2 = serializers.CharField(max_length=128, write_only=True)
    date_birth = serializers.DateField()

    city = serializers.PrimaryKeyRelatedField(
        queryset=City.objects.all(), required=False
    )
    image = serializers.ImageField(required=False)
    lat = serializers.DecimalField(
        decimal_places=6, max_digits=10, required=False
    )
    long = serializers.DecimalField(
        decimal_places=6, max_digits=10, required=False
    )

    token = serializers.CharField(read_only=True, source='key')

    def validate(self, attrs):
        lat = attrs.get('lat')
        lng = attrs.get('long')

        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError(
                _('Enter the same password as above, for verification.')
            )

        if lat or lng:
            if not (lat and lng):
                raise serializers.ValidationError(
                    _('long and lat attributes must be provided together.')
                )
        return attrs

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                _('A user with that username already exists.')
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                _('A user with that email already exists.')
            )
        return value

    def create(self, validated_data):
        instance = User.objects.create_user(**validated_data)
        return SignUpModelProxy(instance).build()


class OAuthConnectSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    fullname = serializers.CharField(
        max_length=128, min_length=1, required=False, allow_blank=True
    )
    sex = SexField(required=False, allow_null=True)
    date_birth = serializers.DateField(required=False, allow_null=True)

    def validate(self, attrs):
        provider_name = self.context['view'].kwargs.get('provider_name')

        if not provider_name:
            raise serializers.ValidationError(_('Not specified provider name'))

        if provider_name not in registry.keys():
            raise serializers.ValidationError(
                'Unknown provider name: {}'.format(provider_name)
            )

        access_token = attrs.pop('access_token')
        provider = registry.get(provider_name)
        try:
            user = provider.connect(access_token, attrs)
        except RequiredFieldsException as e:
            raise serializers.ValidationError({'required_fields': e.args[0]})
        except ProviderException:
            raise serializers.ValidationError(
                _('Unable to connect with provider')
            )
        except UnableRetrieveRequiredData:
            raise serializers.ValidationError(
                _('Unable to retrieve required data')
            )
        return {'user': user}
