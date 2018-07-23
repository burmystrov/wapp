# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from common.filters import UserFilterBackend
from usersettings.models import UserSettings
from usersettings.serializers import UserSettingsSerializer


class UserSettingsViewSet(mixins.UpdateModelMixin,
                          viewsets.ReadOnlyModelViewSet):
    filter_backends = (UserFilterBackend,)
    permission_classes = (IsAuthenticated,)
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer
