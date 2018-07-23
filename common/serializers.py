# encoding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from rest_auth.serializers import PasswordResetSerializer


class PasswordResetHtmlSerializer(PasswordResetSerializer):

    def save(self):
        request = self.context.get('request')
        # Set some values to trigger the send_email method.
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
            'html_email_template_name':
                'registration/password_reset_email_html.html'
        }
        self.reset_form.save(**opts)
