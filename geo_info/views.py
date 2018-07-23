# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet

from common.mixin.views import CountFieldMixin

from .models import City, Country
from .serializers import (AdminCitySerializer, AdminCountrySerializer,
                          CitySerializer, CountrySerializer)


class GeoInfoMixin(CountFieldMixin, ReadOnlyModelViewSet):
    filter_backends = [filters.DjangoFilterBackend, filters.SearchFilter]
    search_fields = ('name_en', 'name_ru')
    ordering_fields = ('count',)


class CountryView(GeoInfoMixin):
    queryset = Country.objects.filter(is_active=True).order_by('-id')
    count_field_name = 'user_countries'
    admin_serializer_class = AdminCountrySerializer
    serializer_class = CountrySerializer


class CityView(GeoInfoMixin):
    queryset = City.objects.filter(country__is_active=True)
    count_field_name = 'user_cities'
    admin_serializer_class = AdminCitySerializer
    serializer_class = CitySerializer
    filter_fields = ('country',)
