# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class ConsumablesCategories(models.Model):
    name = models.CharField(_('name'), max_length=128)
    user = models.ForeignKey(
        'accounts.User', verbose_name=_('user'),
        related_name='user_consumables')
    is_active = models.BooleanField(_('active'), default=True)
    is_general = models.BooleanField(_('general'), default=False)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return 'User ID #{} - {}'.format(self.user_id, self.name)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not ConsumablesCategories.objects.filter(
                name=self.name, user=self.user).exists():
            super(ConsumablesCategories, self).save(
                force_insert=False, force_update=False, using=None,
                update_fields=None
            )


@python_2_unicode_compatible
class Consumables(TimeStampedModel):
    category = models.ForeignKey(
        'consumables.ConsumablesCategories', verbose_name=_('category'),
        related_name='category_consumables')
    description = models.TextField(_('description'), blank=True)
    image = models.ImageField(
        _('image'), upload_to='consumables/images', blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    name = models.CharField(_('name'), max_length=128)
    user_car = models.ForeignKey('usercars.UserCars', verbose_name=_('car'),
                                 related_name='car_consumables')

    def __str__(self):
        return 'Car ID #{} - {}'.format(self.user_car_id, self.name)

    class Meta:
        verbose_name = _('Consumable')
        verbose_name_plural = _('Consumables')
