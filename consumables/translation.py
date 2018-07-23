# encoding: utf-8
from __future__ import unicode_literals

from modeltranslation.translator import translator

from common.mixin.translation import NameTranslation

from .models import ConsumablesCategories

translator.register(ConsumablesCategories, NameTranslation)
