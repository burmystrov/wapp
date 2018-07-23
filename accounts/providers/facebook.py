# encoding: utf-8
from __future__ import unicode_literals

from .base import BaseProvider
from ..models import Profile


class Provider(BaseProvider):
    BASE_URL = 'https://graph.facebook.com/'
    AUTHORIZE_URL = 'https://graph.facebook.com/oauth/authorize'
    ACCESS_TOKEN_URL = 'https://graph.facebook.com/v2.3/oauth/access_token'

    def normalize_me(self, data):
        fullname = '{} {}'.format(data.get('first_name'), data.get('last_name'))
        return {
            'id': data.get('id'),
            'email': data.get('email'),
            'fullname': fullname,
            'sex': self.get_gender(data),
        }

    def get_gender(self, data):
        gender = data.get('gender')
        if gender:
            if gender == 'male':
                return Profile.MALE
            elif gender == 'female':
                return Profile.FEMALE
