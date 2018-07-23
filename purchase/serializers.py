# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from rest_framework import serializers

from .models import Purchases


class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = (
            'receipt_data', 'transaction_date', 'transaction_state',
            'transaction_id'
        )
