# encoding: utf-8
from __future__ import unicode_literals

import pytz
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


class Base(models.Model):
    geoname_id = models.IntegerField(unique=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Country(Base):
    OCEANIA = 'OC'
    EUROPE = 'EU'
    AFRICA = 'AF'
    NORTH_AMERICA = 'NA'
    SOUTH_AMERICA = 'SA'
    ANTARCTICA = 'AN'
    ASIA = 'AS'

    CONTINENT_CHOICES = (
        (OCEANIA, _('Oceania')),
        (EUROPE, _('Europe')),
        (AFRICA, _('Africa')),
        (NORTH_AMERICA, _('North America')),
        (ANTARCTICA, _('Antarctica')),
        (SOUTH_AMERICA, _('South America')),
        (ASIA, _('Asia')),
    )

    name = models.CharField(max_length=200, unique=True, db_index=True)
    code2 = models.CharField(max_length=2, unique=True)
    code3 = models.CharField(max_length=3, unique=True)
    timezone = models.CharField(
        max_length=64, blank=True,
        choices=((tz, tz) for tz in pytz.all_timezones)
    )
    tld = models.CharField(max_length=5, blank=True, db_index=True)
    continent = models.CharField(
        max_length=2, db_index=True, choices=CONTINENT_CHOICES
    )
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Region(Base):
    name = models.CharField(max_length=200, db_index=True)
    geoname_code = models.CharField(max_length=50, db_index=True)
    country = models.ForeignKey('Country')


@python_2_unicode_compatible
class City(Base):
    name = models.CharField(max_length=200, db_index=True)
    region = models.ForeignKey('Region', blank=True, null=True)
    country = models.ForeignKey('Country')

    def __str__(self):
        return self.name
