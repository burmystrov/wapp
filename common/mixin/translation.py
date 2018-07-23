# encoding: utf-8
from __future__ import unicode_literals

from modeltranslation.translator import TranslationOptions


class NameTranslation(TranslationOptions):
    fields = ('name',)
    empty_values = {'name': None}
