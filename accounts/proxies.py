# encoding: utf-8
from __future__ import unicode_literals

from common.proxies import ModelProxy


class SignUpModelProxy(ModelProxy):
    fields = ['id', 'username', 'email']
    nested_fields = {
        'profile': ['fullname', 'sex', 'date_birth', 'city', 'image'],
        'auth_token': ['key']
    }
