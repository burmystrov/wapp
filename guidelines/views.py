# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Guidelines
from .serializers import GuidelinesSerializer


class GuidelinesViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = GuidelinesSerializer
    queryset = Guidelines.objects.all()
    permission_classes = (IsAuthenticated,)
