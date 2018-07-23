# encoding: utf-8
from __future__ import unicode_literals

from rest_framework.permissions import BasePermission


class UserObjectPermission(BasePermission):
    user_field = 'user'

    def has_object_permission(self, request, view, obj):
        return (getattr(obj, self.user_field) == request.user or
                request.user.is_staff)
