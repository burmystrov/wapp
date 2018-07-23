# encoding: utf-8
from __future__ import unicode_literals

import itunesiap
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Purchases
from .serializers import PurchasesSerializer


class PurchasesViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer
    permission_classes = (IsAuthenticated, )
    message_error = _('receipt_data a not valid')

    def get_regime_working(self):
        return itunesiap.env.unsafe \
            if settings.DEBUG else itunesiap.env.production

    def send_to_check_itunes(self, receipt_data):
        try:
            with self.get_regime_working():
                response = itunesiap.verify(
                    receipt_data, password=settings.ITUNES_PASSWORD)
        except itunesiap.exc.InvalidReceipt:
            response = None
        return response

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.initial_data

        if data and data.get('receipt_data'):
            resp = self.send_to_check_itunes(data.get('receipt_data'))
            if resp:

                transaction_id_response = resp.receipt.last_in_app.\
                    transaction_id
                transaction_id_request = data.get('transaction_id')

                if transaction_id_response == transaction_id_request and \
                        not Purchases.objects.filter(
                            transaction_id=transaction_id_response).exists():

                    serializer.save(
                        user=request.user, response=resp, is_check=True
                    )
                    headers = self.get_success_headers(serializer.data)
                    data_response = {
                        'transaction_date':
                            serializer.data.get('transaction_date'),
                        'transaction_state':
                            serializer.data.get('transaction_state'),
                        'transaction_id': serializer.data.get('transaction_id'),
                    }
                    return Response(
                        data_response, status=status.HTTP_201_CREATED,
                        headers=headers
                    )
                self.message_error = _('transaction_id is not correct')

        return Response(
            {'error': self.message_error},
            status=status.HTTP_400_BAD_REQUEST
        )
