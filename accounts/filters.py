from __future__ import unicode_literals

import rest_framework_filters as filters
from django.contrib.auth import get_user_model


class UserFilter(filters.FilterSet):
    date_from = filters.DateFilter(name='date_joined', lookup_type='gte')
    date_to = filters.DateFilter(name='date_joined', lookup_type='lte')

    class Meta:
        model = get_user_model()
        fields = ('date_from', 'date_to')
