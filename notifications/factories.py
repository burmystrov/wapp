# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

import random

import factory
from faker import Factory as FakerFactory
from push_notifications.models import APNSDevice, GCMDevice

from accounts.factories import UserFactory
from common.fake import date
from notifications.models import NotificationOptions

faker = FakerFactory.create()


class GCMDeviceFactory(factory.DjangoModelFactory):
    @factory.lazy_attribute_sequence
    def registration_id(self, n):
        return 'registration id {}'.format(n)

    @factory.lazy_attribute
    def active(self):
        return random.choice([True, False])

    @factory.lazy_attribute
    def user(self):
        return factory.SubFactory(UserFactory)

    class Meta(object):
        model = GCMDevice


class APNSDeviceFactory(factory.DjangoModelFactory):
    @factory.lazy_attribute_sequence
    def registration_id(self, n):
        return 'AE' * 30 + '{:04x}'.format(n)

    @factory.lazy_attribute
    def active(self):
        return random.choice([True, False])

    @factory.lazy_attribute
    def user(self):
        return factory.SubFactory(UserFactory)

    class Meta(object):
        model = APNSDevice


class NotificationOptionsFactory(factory.DjangoModelFactory):
    last_push = factory.lazy_attribute(lambda x: date())

    @factory.lazy_attribute
    def user(self):
        return factory.SubFactory(UserFactory)

    @factory.lazy_attribute
    def name(self):
        return random.choice([
            NotificationOptions.Names.MILEAGE,
            NotificationOptions.Names.MAINTENANCE1,
            NotificationOptions.Names.MAINTENANCE2
        ])

    @factory.lazy_attribute
    def period(self):
        if self.name == NotificationOptions.Names.MILEAGE:
            return random.choice(NotificationOptions.Periods.Mileage.ALL)
        return random.choice(NotificationOptions.Periods.Maintenance.ALL)

    @factory.lazy_attribute
    def is_active(self):
        return random.choice([True, False])

    class Meta:
        model = NotificationOptions
