# encoding: utf-8
from __future__ import unicode_literals

from collections import OrderedDict

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse


class APIRoot(APIView):
    permission_classes = ()

    def get(self, request):
        urls_list = [
            ('accounts', {
                'users': reverse('users-list', request=request),
                'profiles': reverse('profiles-list', request=request),
                'countries': reverse('countries-list', request=request),
                'cities': reverse('cities-list', request=request),
                'cars': reverse('cars-list', request=request),
                'car-mileages': reverse('car-mileages-list', request=request),
                'location-images': reverse(
                    'location-images-list', request=request)
            }),
            ('auth', {
                'login': reverse('login', request=request),
                'registration': reverse('registration', request=request),
                'password-reset': reverse('rest_password_reset',
                                          request=request),
                'password-change': reverse('rest_password_change',
                                           request=request),
            }),
            ('brands', {
                'brands': reverse('brands-list', request=request),
                'models': reverse('models-list', request=request),
            }),
            ('consumables', {
                'consumables': reverse('consumables-list', request=request),
                'consumables-categories': reverse(
                    'consumables_categories-list', request=request),
            }),
            ('devices', {
                'android': reverse('android-devices-list', request=request),
                'ios': reverse('ios-devices-list', request=request),
            }),
            ('guidelines', {
                'list': reverse('guidelines-list', request=request),
            }),
            ('maintenances', {
                'maintenances': reverse('maintenances-list', request=request),
                'additional-maintenances': reverse(
                    'additional_maintenances-list', request=request)
            }),
            ('notifications', {
                'notification-options': reverse(
                    'notification-options-list', request=request)
            }),
            ('purchase', {
                'purchase': reverse(
                    'purchases-list', request=request)
            }),
            ('triggers', {
                'open-app': reverse(
                    'open_app_trigger', request=request)
            }),
            ('usersettings', {
                'list': reverse('user-settings-list', request=request),
            }),
        ]
        return Response(OrderedDict(urls_list))


api_root = APIRoot.as_view()
