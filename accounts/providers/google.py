# encoding: utf-8
from __future__ import unicode_literals

from .base import BaseProvider


class Provider(BaseProvider):
    BASE_URL = 'https://www.googleapis.com/plus/v1/people/'
    AUTHORIZE_URL = 'https://accounts.google.com/o/oauth2/auth'
    ACCESS_TOKEN_URL = 'https://www.googleapis.com/oauth2/v3/token'

    def normalize_me(self, data):
        emails = data.get('emails')
        if emails and isinstance(emails, (list, tuple)):
            email = emails[0]['value']
        else:
            email = None
        return {
            'id': data.get('id'),
            'email': email,
            'fullname': data.get('displayName'),
        }
