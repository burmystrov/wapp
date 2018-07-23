# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from push_notifications.models import APNSDevice, GCMDevice
from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from common.filters import UserFilterBackend
from common.permissions import UserObjectPermission
from notifications.models import NotificationOptions
from notifications.serializers import (NotificationOptionsSerializer,
                                       RegisterAPNSDeviceSerializer,
                                       RegisterGCMDeviceSerializer)


class DeviceViewSetMixin(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, UserObjectPermission)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated():
            serializer.save(user=self.request.user)


class RegisterGCMDeviceViewSet(DeviceViewSetMixin):
    serializer_class = RegisterGCMDeviceSerializer
    queryset = GCMDevice.objects.all()


class RegisterAPNSDeviceViewSet(DeviceViewSetMixin):
    serializer_class = RegisterAPNSDeviceSerializer
    queryset = APNSDevice.objects.all()


class NotificationOptionViewSet(mixins.UpdateModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.ListModelMixin,
                                GenericViewSet):
    filter_backends = (UserFilterBackend, )
    permission_classes = (permissions.IsAuthenticated, )
    queryset = NotificationOptions.objects.all()
    serializer_class = NotificationOptionsSerializer
