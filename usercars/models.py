# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.fields import AutoCreatedField
from model_utils.models import TimeStampedModel

from accounts.models import User
from common.models import LocationMixin
from common.utils import date_now, date_to_timestamp, send_notifications
from constans import NAME_NOTIFICATIONS
from notifications.params import ParamsForNextMaintenances
from typecars.models import Models


@python_2_unicode_compatible
class UserCars(TimeStampedModel):

    class MileageFrequencies(object):
        """
        Enumeration class stores available choices for maintenance frequency
        depending on mileage since last maintenance.
        """
        FIVE = 5
        TEN = 10
        FIFTEEN = 15
        TWENTY = 20
        TWENTY_FIVE = 25
        THIRTY = 30
        CHOICES = (
            (FIVE, _('5.000 km')),
            (TEN, _('10.000 km')),
            (FIFTEEN, _('15.000 km')),
            (TWENTY, _('20.000 km')),
            (TWENTY_FIVE, _('25.000 km')),
            (THIRTY, _('30.000 km')),
        )

    class DateFrequencies(object):
        """
        Enumeration class stores available choices for maintenance frequency
        depending on time since last maintenance.
        """
        ONE_YEAR = 1
        TWO_YEARS = 2
        CHOICES = (
            (ONE_YEAR, _('one year')),
            (TWO_YEARS, _('two years')),
        )

    user = models.ForeignKey(User, related_name='user_cars')
    model = models.ForeignKey(Models, related_name='model_cars')
    model_year = models.CharField(_('year of manufacture'), max_length=4)
    current_mileage = models.PositiveIntegerField()
    last_service_date = models.DateField(blank=True, null=True)
    last_service_mileage = models.PositiveIntegerField(blank=True, null=True)
    #: Define maintenance frequency depending on mileage since last maintenance.
    frequency_run = models.IntegerField(
        choices=MileageFrequencies.CHOICES, blank=True,
        default=MileageFrequencies.TWENTY)
    #: Define maintenance frequency depending on time since last maintenance.
    date_next_to = models.IntegerField(
        choices=DateFrequencies.CHOICES, blank=True,
        default=DateFrequencies.ONE_YEAR)
    next_maintenances_new = models.FloatField(blank=True, null=True)
    next_maintenances_old = models.FloatField(blank=True, null=True)
    #: Meta field to track for mileage updates.
    mileage_update = AutoCreatedField()

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')
        ordering = ('-id',)

    def __str__(self):
        return 'ID #{} -  User ID #{} - Model ID #{}'.format(
            self.id, self.user_id, self.model_id
        )

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        nm = ParamsForNextMaintenances(self)
        self.next_maintenances_new = date_to_timestamp(
            nm.optimum_maintenance_event_date()
        )
        super(UserCars, self).save(force_insert=False, force_update=False,
                                   using=None, update_fields=None)


class LocationImages(LocationMixin, TimeStampedModel):
    name = models.CharField(max_length=128)
    image = models.ImageField(upload_to='location_images/%Y/%m/%d')
    user_car = models.ForeignKey(UserCars, related_name='car_images')
    is_main = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        skip_reset = kwargs.pop('skip_reset', None)
        if not skip_reset:
            qs = LocationImages.objects.filter(user_car=self.user_car)

            if not qs.count():
                self.is_main = True
            elif self.is_main:
                qs.update(is_main=False)
        super(LocationImages, self).save(*args, **kwargs)

    def delete(self, using=None):
        if self.is_main:
            obj = (LocationImages.objects.filter(user_car=self.user_car).
                   exclude(id=self.pk).first())
            if obj:
                obj.is_main = True
                obj.save(update_fields=['is_main'], skip_reset=True)
        super(LocationImages, self).delete(using)

    class Meta:
        ordering = ('-id',)


@receiver(post_save, sender=UserCars, dispatch_uid='send_push_main')
def send_push_main(sender, instance=None, created=False, **kwargs):
    nmn = instance.next_maintenances_new
    nmo = instance.next_maintenances_old
    if not created and nmn != nmo:
        car = {
            'notifications': {
                'timestamp': nmn,
                'name': NAME_NOTIFICATIONS.get(0)
            },
            'car': {
                'id': instance.pk,
                'model': instance.model.name
            }
        }
        send_notifications(user=instance.user, extra=car)
        instance.next_maintenances_old = nmn
        instance.save(update_fields=['next_maintenances_old'])
