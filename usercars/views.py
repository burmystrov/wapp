# encoding: utf-8
from __future__ import unicode_literals

from rest_framework import filters, mixins, permissions, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from common.filters import UserCarFilterBackend, UserFilterBackend
from usercars.filters import UserCarsFilter
from usercars.models import LocationImages, UserCars
from usercars.serializers import (CarMileageSerializer,
                                  LocationImageSerializer,
                                  UpdateLocationImageSerializer,
                                  UserCarsSerializer)


class UserCarsViewSet(ModelViewSet):
    """
    Returns a list of all cars that belongs to logged in user.
    """
    filter_backends = (UserFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserCars.objects.all()
    serializer_class = UserCarsSerializer

    def filter_queryset(self, queryset):
        self.filter_class = (UserCarsFilter if self.request.user.is_superuser
                             else None)
        return super(UserCarsViewSet, self).filter_queryset(queryset)

    def create(self, request, *args, **kwargs):
        if not request.user.is_able_to_add_car():
            msg = 'Unable to add this car due to exceeding limit for your plan'
            return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)
        return super(UserCarsViewSet, self).create(request, *args, **kwargs)


class CarMileageView(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     GenericViewSet):
    """
    Returns a list of all user cars' mileages.
    """
    filter_backends = (UserFilterBackend,)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = UserCars.objects.all()
    serializer_class = CarMileageSerializer


class LocImageViewSet(ModelViewSet):
    filter_backends = (
        UserCarFilterBackend,
        filters.DjangoFilterBackend,
        filters.SearchFilter, )
    filter_fields = ('user_car',)
    permission_classes = (permissions.IsAuthenticated,)
    queryset = LocationImages.objects.all()
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return UpdateLocationImageSerializer

        return LocationImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_car = serializer.validated_data['user_car']
        if not request.user.is_able_to_add_image(user_car.id):
            msg = 'Unable to add this image due to exceeding limit ' \
                  'for your plan'
            return Response({'error': msg}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        keys_data = request.data.keys()
        if not 'image' in keys_data:
            request.data['image'] = instance.image
        if not 'is_main' in keys_data:
            request.data['is_main'] = instance.is_main
        if not 'name' in keys_data:
            request.data['name'] = instance.name
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
