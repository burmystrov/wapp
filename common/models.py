# encoding: utf-8
from __future__ import unicode_literals

from django.db import models


class IsActiveMixin(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class LocationMixin(models.Model):
    lat = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True
    )
    long = models.DecimalField(
        max_digits=10, decimal_places=6, blank=True, null=True
    )

    class Meta:
        abstract = True
