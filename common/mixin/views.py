# encoding: utf-8
from __future__ import unicode_literals

from django.db.models import Count
from rest_framework import filters


class CountFieldMixin(object):
    """
    Adds extra field count for superuser
    """
    count_field_name = None
    admin_serializer_class = None

    def filter_queryset(self, queryset):
        if self.request.user.is_superuser:
            filter_backends = self.filter_backends + [filters.OrderingFilter]
        else:
            filter_backends = self.filter_backends

        for backend in list(filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        return queryset

    def get_queryset(self):
        qs = super(CountFieldMixin, self).get_queryset()
        assert self.count_field_name is not None, (
            '`count_field_name` must be declared in class'
            ' `{}`'.format(self.__class__.__name__)
        )
        return (qs.annotate(count=Count(self.count_field_name))
                if self.request.user.is_superuser else qs)

    def get_serializer_class(self):
        assert self.admin_serializer_class and self.serializer_class, (
            'Properties `admin_serializer_class` and `serializer_class` '
            'must be declared in class `{}`'.format(self.__class__.__name__)
        )
        return (self.admin_serializer_class if self.request.user.is_superuser
                else self.serializer_class)


class QuerySetUserCarMixin(object):
    def get_queryset(self):
        user = self.request.user
        qs = super(QuerySetUserCarMixin, self).get_queryset()
        return qs if user.is_superuser else qs.filter(user_car__user=user)
