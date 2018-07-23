# encoding: utf-8
from __future__ import unicode_literals

from rest_framework.permissions import SAFE_METHODS, IsAuthenticated


class ConsumablesCategoriesPermission(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return (request.user == obj.user or request.method in SAFE_METHODS and
                obj.is_general or request.user.is_superuser)
