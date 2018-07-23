# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from common.mixin.views import CountFieldMixin

from .models import Brands, Models
from .serializers import (AdminBrandSerializer, AdminModelSerializer,
                          BrandSerializer, ModelSerializer)


class BrandsView(CountFieldMixin, ReadOnlyModelViewSet):
    queryset = Brands.objects.filter(is_active=True)
    count_field_name = 'brand_models__model_cars'
    admin_serializer_class = AdminBrandSerializer
    serializer_class = BrandSerializer
    filter_fields = ('name',)
    filter_backends = [filters.DjangoFilterBackend]
    ordering_fields = ('count')
    permission_classes = (IsAuthenticated,)


class ModelsView(CountFieldMixin, ReadOnlyModelViewSet):
    queryset = Models.objects.filter(is_active=True)
    count_field_name = 'model_cars'
    admin_serializer_class = AdminModelSerializer
    serializer_class = ModelSerializer
    filter_backends = [filters.DjangoFilterBackend]
    ordering_fields = ('count',)
    permission_classes = (IsAuthenticated,)
    filter_fields = ('name', 'brand__name')
