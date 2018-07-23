# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

import factory
from django.conf import settings
from factory.fuzzy import FuzzyChoice

from .models import UserSettings


class UserSettingsFactory(factory.DjangoModelFactory):
    lang = FuzzyChoice(map(lambda l: l[0], settings.LANGUAGES))
    date_format = FuzzyChoice(map(lambda f: f[0],
                                  UserSettings.TimeFormat.CHOICES))

    class Meta(object):
        model = UserSettings
