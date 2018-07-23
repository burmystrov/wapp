# encoding: utf-8
from __future__ import unicode_literals

import importlib

from django.conf import settings


def register_providers():
    """Registers all providers which are declared in settings"""
    providers = {}

    assert hasattr(settings, 'SOCIAL_PROVIDERS'), (
        'SOCIAL_PROVIDERS is not declared in settings'
    )
    for name in settings.SOCIAL_PROVIDERS:
        if name not in providers:
            module = importlib.import_module('.{}'.format(name), __package__)
            providers[name] = module.Provider(name)
    return providers


registry = register_providers()
