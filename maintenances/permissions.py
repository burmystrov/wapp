# encoding: utf-8
from __future__ import unicode_literals

from rest_framework.permissions import (SAFE_METHODS, BasePermission,
                                        IsAuthenticated)


class AdditionalMaintenancesPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_superuser and request.method in SAFE_METHODS or
                not request.user.is_superuser and request.user.is_paid)

    def has_object_permission(self, request, view, obj):
        return request.user == obj.am.user_car.user and request.user.is_paid


class MaintenancesPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user_car.user
