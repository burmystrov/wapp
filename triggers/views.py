# encoding: utf-8
from __future__ import unicode_literals

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from common.utils import send_notifications
from constans import NAME_NOTIFICATIONS
from usercars.models import UserCars


class OpenAppView(GenericAPIView):
    serializer_class = Serializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        push = False
        user = request.user
        cars = UserCars.objects.filter(user=user)
        if cars.exists():
            cars = [
                {
                    'notifications': {
                        'timestamp': car.next_maintenances_new,
                        'name': NAME_NOTIFICATIONS.get(0)
                    },
                    'car': {
                        'id': car.id,
                        'model': car.model.name
                    }
                }
                for car in cars
            ]
            send_notifications(user=user, message=None, extra=cars)
            push = True
        return Response({'push': push})
