# encoding: utf-8
from __future__ import unicode_literals

import factory
from factory.fuzzy import FuzzyInteger
from faker import Factory as FakerFactory

from accounts.factories import UserFactory
from common.fake import date
from typecars.factories import ModelsFactory

from .models import LocationImages, UserCars

faker = FakerFactory.create()


class UserCarsFactory(factory.DjangoModelFactory):
    class Meta:
        model = UserCars

    user = factory.SubFactory(UserFactory)
    model = factory.SubFactory(ModelsFactory)
    model_year = FuzzyInteger(1980, 2015)
    current_mileage = FuzzyInteger(0, 1000000)
    last_service_mileage = FuzzyInteger(0, 1000000)


class LocationImagesFactory(factory.DjangoModelFactory):
    class Meta:
        model = LocationImages

    name = factory.lazy_attribute(lambda x: faker.name())
    image = factory.django.ImageField(width=600)
    user_car = factory.SubFactory(UserCarsFactory)
