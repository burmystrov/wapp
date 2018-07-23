# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from common.utils import datetime_to_timestamp


class MaintenancesManager(models.Manager):
    def get_queryset(self):
        """
        Hide maintenances for internal uses.
        """
        return super(MaintenancesManager, self).get_queryset()


@python_2_unicode_compatible
class Maintenances(models.Model):
    class Type(object):
        """
        Enumeration class with available values of type attribute.
        """
        #: Initial maintenance used in internal purposes and should not be
        #: included in API output. It is used to save initial values of mileage.
        SCHEDULED = 'Scheduled'
        UNPLANNED = 'Unplanned'

        CHOICES = (
            (SCHEDULED, _('Scheduled')),
            (UNPLANNED, _('Unplanned'))
        )

    objects = MaintenancesManager()
    default_manager = models.Manager()

    datetime = models.DateTimeField(_('datetime'))
    description = models.TextField(_('description'), blank=True)
    name = models.CharField(_('name'), max_length=128)
    mileage_to = models.PositiveIntegerField(_('mileage'))
    type = models.CharField(_('type'), choices=Type.CHOICES, max_length=15)
    user_car = models.ForeignKey('usercars.UserCars', verbose_name=_('car'),
                                 related_name='car_maintenances')

    class Meta:
        verbose_name = _('Maintenance')
        verbose_name_plural = _('Maintenances')

    def __str__(self):
        return 'Car ID #{} - {}'.format(self.user_car_id, self.name)


@python_2_unicode_compatible
class AdditionalMaintenances(models.Model):
    am = models.OneToOneField(
        'maintenances.Maintenances', verbose_name=_('maintenance'),
        related_name='maintenance_additional', primary_key=True)
    description = models.TextField(_('description'), blank=True)
    lat = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True)
    lon = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True)
    name_master = models.TextField(_('name'), blank=True)
    phone_master = models.CharField(_('phone'), max_length=128)

    class Meta:
        verbose_name = _('Additional')
        verbose_name_plural = _('Additionals')

    def __str__(self):
        return 'Maintenances ID #{} - {}'.format(self.am_id, self.phone_master)


@receiver(post_save, sender=Maintenances, dispatch_uid='additional_add')
def additional_add(sender, instance=None, created=False, **kwargs):
    last_maintenances = Maintenances.objects.filter(
        user_car=instance.user_car, type=Maintenances.Type.SCHEDULED
    ).order_by('-datetime').first()
    if last_maintenances:
        lmd = last_maintenances.datetime
        lmm = last_maintenances.mileage_to
        if ((instance.user_car.last_service_date != lmd) or
                (instance.user_car.last_service_mileage != lmm)):
            instance.user_car.last_service_date = lmd.date()
            instance.user_car.last_service_mileage = lmm
            instance.user_car.save(
                update_fields=['last_service_date', 'last_service_mileage']
            )
    if created:
        AdditionalMaintenances.objects.create(am=instance)
