# encoding: utf-8
from __future__ import unicode_literals

import rest_framework_filters as filters

from .models import UserCars


class UserCarsFilter(filters.FilterSet):
    created_from = filters.DateFilter(name='created', lookup_type='gte')
    created_to = filters.DateFilter(name='created', lookup_type='lte')

    class Meta:
        model = UserCars
        fields = ('created_from', 'created_to')
