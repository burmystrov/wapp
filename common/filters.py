# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from rest_framework.filters import BaseFilterBackend


class UserFilterBackend(BaseFilterBackend):
    """
    Filter set of objects, retrieving only objects that belongs to logged in
    user.

    Note:
    * This filter should be applied very first, so it should be first in the
      list of `filter_backends`.
    * It doesn't check if user is authenticated so you should add
      `IsAuthenticated` permission as well.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user=request.user)


class UserCarFilterBackend(BaseFilterBackend):
    """
    Filter set of objects, retrieving only objects that related to cars which
    belongs to logged in user.

    Note:
    * This filter should be applied very first, so it should be first in the
      list of `filter_backends`.
    * It doesn't check if user is authenticated so you should add
      `IsAuthenticated` permission as well.
    """
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(user_car__user=request.user)
