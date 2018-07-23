# encoding: utf-8
from __future__ import unicode_literals

import datetime

import factory
from django.utils.timezone import now
from factory.fuzzy import FuzzyChoice, FuzzyInteger

from usercars.factories import UserCarsFactory

from .models import AdditionalMaintenances, Maintenances


class MaintenancesFactory(factory.DjangoModelFactory):
    datetime = factory.fuzzy.FuzzyDateTime((
        now() - datetime.timedelta(days=356)
    ))
    description = factory.LazyAttributeSequence(
        lambda o, n: 'maintance #{} description'.format(n))
    mileage_to = FuzzyInteger(1000)
    name = factory.LazyAttributeSequence(
        lambda o, n: 'maintenance {}'.format(n))
    type = FuzzyChoice(map(lambda t: t[1], Maintenances.Type.CHOICES))
    user_car = factory.SubFactory(UserCarsFactory)

    class Meta:
        model = Maintenances


class AdditionalMaintenancesFactory(factory.DjangoModelFactory):
    am = factory.SubFactory(MaintenancesFactory)
    description = factory.LazyAttributeSequence(
        lambda o, n: 'additional maintance #{} description'.format(n))
    lat = factory.fuzzy.FuzzyDecimal(0, 180, 6)
    lon = factory.fuzzy.FuzzyDecimal(0, 360, 6)
    phone_master = factory.LazyAttributeSequence(
        lambda o, n: '+38068{:0>7}'.format(n)
    )

    class Meta:
        model = AdditionalMaintenances
