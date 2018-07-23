# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from model_utils.models import TimeStampedModel

from accounts.models import User


@python_2_unicode_compatible
class Purchases(TimeStampedModel):
    user = models.ForeignKey('accounts.User', verbose_name='user_purchases')
    receipt_data = models.TextField()
    transaction_id = models.CharField(max_length=128)
    transaction_date = models.DateTimeField()
    transaction_state = models.CharField(max_length=128)
    response = models.TextField(blank=True)
    is_check = models.BooleanField(default=False)

    def __str__(self):
        return 'User #{}'.format(self.user_id)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_check:
            User.objects.filter(id=self.user_id).update(is_paid=True)
        super(Purchases, self).save(
            force_insert=False, force_update=False, using=None,
            update_fields=None
        )
