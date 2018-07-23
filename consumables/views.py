# encoding: utf-8
from __future__ import unicode_literals

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from common.filters import UserCarFilterBackend
from common.mixin.views import CountFieldMixin, QuerySetUserCarMixin
from consumables.models import Consumables, ConsumablesCategories
from consumables.permissions import ConsumablesCategoriesPermission
from consumables.serializers import (AdminConsumablesCategoriesSerializer,
                                     ConsumablesCategoriesSerializer,
                                     ConsumablesSerializer)


class ConsumablesCategoriesView(CountFieldMixin, viewsets.ModelViewSet):
    queryset = ConsumablesCategories.objects.select_related()
    admin_serializer_class = AdminConsumablesCategoriesSerializer
    serializer_class = ConsumablesCategoriesSerializer
    count_field_name = 'category_consumables'
    filter_fields = ('name',)
    ordering_fields = ('count',)
    permission_classes = (ConsumablesCategoriesPermission,)

    def perform_create(self, serializer):
        user = self.request.user
        is_general = True if user.is_superuser else False
        serializer.save(user=user, is_general=is_general)

    def get_queryset(self):
        user = self.request.user
        qs = super(ConsumablesCategoriesView, self).get_queryset()
        return (qs if user.is_superuser else
                qs.filter(Q(is_general=True) | Q(user=user)))


class ConsumablesView(QuerySetUserCarMixin, viewsets.ModelViewSet):
    filter_backends = (UserCarFilterBackend,)
    filter_fields = ('name', 'user_car', 'category')
    queryset = Consumables.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ConsumablesSerializer
