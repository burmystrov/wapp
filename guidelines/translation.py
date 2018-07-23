# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from modeltranslation.translator import TranslationOptions, translator

from .models import Guidelines


class GuidelinesTranslation(TranslationOptions):
    fields = ('name', 'file_video')


translator.register(Guidelines, GuidelinesTranslation)
