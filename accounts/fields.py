# encoding: utf-8
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from .models import Profile


class SexField(serializers.Field):
    default_error_messages = {
        'invalid': _('"{input}" is not a valid value.')
    }

    def to_representation(self, value):
        return Profile.get_sex_name_by_id(value)

    def to_internal_value(self, data):
        idx = Profile.get_sex_id_by_name(data)
        if idx is not None:
            return idx

        self.fail('invalid', input=data)
