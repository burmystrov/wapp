# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import mixins, viewsets

from common.mixin.views import QuerySetUserCarMixin

from .models import AdditionalMaintenances, Maintenances
from .permissions import (AdditionalMaintenancesPermission,
                          MaintenancesPermission)
from .serializers import (AdditionalMaintenancesSerializer,
                          MaintenancesSerializer)


class MaintenancesView(QuerySetUserCarMixin, viewsets.ModelViewSet):
    serializer_class = MaintenancesSerializer
    filter_fields = ('user_car', 'type', 'name')
    permission_classes = (MaintenancesPermission,)

    def get_queryset(self):
        user = self.request.user
        qs = Maintenances.objects.select_related()
        return qs.filter(user_car__user=user)


class AdditionalMaintenancesView(mixins.RetrieveModelMixin,
                                 mixins.UpdateModelMixin,
                                 mixins.DestroyModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    queryset = AdditionalMaintenances.objects.select_related()
    serializer_class = AdditionalMaintenancesSerializer
    filter_fields = ('am', )
    permission_classes = (AdditionalMaintenancesPermission,)

    def get_queryset(self):
        user = self.request.user
        qs = super(AdditionalMaintenancesView, self).get_queryset()
        return qs if user.is_superuser else qs.filter(am__user_car__user=user)
