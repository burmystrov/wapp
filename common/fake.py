# encoding: utf-8
from __future__ import unicode_literals

import datetime

from faker import Factory as FakerFactory

faker = FakerFactory.create()


def date():
    """Helper for generating fake date"""
    return datetime.date(*map(int, faker.date().split('-')))
