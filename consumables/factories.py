# encoding: utf-8
from __future__ import unicode_literals

import factory
from factory.fuzzy import FuzzyChoice

from accounts.factories import UserFactory
from models import Consumables, ConsumablesCategories
from usercars.factories import UserCarsFactory


class ConsumablesCategoriesFactory(factory.DjangoModelFactory):
    class Meta:
        model = ConsumablesCategories

    name = factory.Sequence(lambda n: 'category%d' % n)
    user = factory.SubFactory(UserFactory)
    is_active = FuzzyChoice([True, False])
    is_general = FuzzyChoice([True, False])


class ConsumablesFactory(factory.DjangoModelFactory):
    class Meta:
        model = Consumables

    name = factory.Sequence(lambda n: 'model%d' % n)
    image = factory.django.ImageField(width=600)
    user_car = factory.SubFactory(UserCarsFactory)
    is_active = FuzzyChoice([True, False])
    category = factory.SubFactory(ConsumablesCategoriesFactory)
