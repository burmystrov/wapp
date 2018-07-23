# encoding: utf-8
from __future__ import unicode_literals

import random

import factory
from faker import Factory as FakerFactory

from common.fake import date

from .models import Profile, User

faker = FakerFactory.create()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.sequence(
        lambda n: '{0}_{1}'.format(faker.user_name(), n)
    )
    email = factory.lazy_attribute(lambda x: faker.email())
    password = 'passwd'


class ProfileFactory(factory.DjangoModelFactory):
    class Meta:
        model = Profile

    image = factory.django.ImageField(width=600)

    fullname = factory.lazy_attribute(lambda x: faker.name())

    date_birth = factory.lazy_attribute(lambda x: date())

    @factory.lazy_attribute
    def sex(self):
        return random.choice([Profile.MALE, Profile.FEMALE])
