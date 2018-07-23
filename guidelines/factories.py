# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

import factory

from .models import Guidelines


class GuidelinesFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'guideline%d' % n)
    file_video = factory.django.FileField(data=b'')

    class Meta:
        model = Guidelines
