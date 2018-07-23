# encoding: utf-8
from __future__ import unicode_literals

import factory
from factory.fuzzy import FuzzyChoice, FuzzyInteger

from .models import Brands, Models


class BrandsFactory(factory.DjangoModelFactory):
    class Meta:
        model = Brands

    name = factory.Sequence(lambda n: 'brand%d' % n)
    image = factory.django.ImageField(width=600)
    is_active = FuzzyChoice([True, False])


class ModelsFactory(factory.DjangoModelFactory):
    class Meta:
        model = Models

    name = factory.Sequence(lambda n: 'model%d' % n)
    image = factory.django.ImageField(width=600)
    brand = factory.SubFactory(BrandsFactory)
