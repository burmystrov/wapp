# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from common.models import IsActiveMixin


@python_2_unicode_compatible
class Brands(IsActiveMixin):
    name = models.CharField(max_length=128, unique=True)
    image = models.ImageField(upload_to='type_cars/brands', blank=True)

    class Meta:
        verbose_name = _('Brand')
        verbose_name_plural = _('Brands')
        ordering = ('-id',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Models(IsActiveMixin):
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

    brand = models.ForeignKey(
        Brands, limit_choices_to={'is_active': True},
        related_name='brand_models'
    )
    name = models.CharField(_('model'), max_length=128)
    image = models.ImageField(upload_to='type_cars/models', blank=True)
    frequency_run = models.IntegerField(
        choices=MileageFrequencies.CHOICES, blank=True,
        default=MileageFrequencies.TEN
    )

    class Meta:
        unique_together = (('brand', 'name'),)
        verbose_name = _('Model')
        verbose_name_plural = _('Models')
        ordering = ['-id']

    def __str__(self):
        return self.name
