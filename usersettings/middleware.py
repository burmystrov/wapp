# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from django.conf import settings
from django.utils import translation
from rest_framework.authtoken.models import Token

from .models import UserSettings


class UserDefinedLocaleMiddleware(object):
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context. This allows pages to be dynamically
    translated to the language the user desires (if the language
    is available, of course).

    Note: to determine current language this middleware should be processed
    after login middleware.
    """
    def process_request(self, request):
        #: Retrieve settings for current user of None.

        if request.user and request.user.is_authenticated():
            usersettings = UserSettings.objects.filter(
                user=request.user).first()
        else:
            usersettings = None
            headers = request.META.get('HTTP_AUTHORIZATION')
            if headers:
                headers = headers.split()
                if len(headers) == 2 and headers[0] == 'Token':
                    tk = Token.objects.filter(key=headers[1])
                    if tk.exists():
                        usersettings = UserSettings.objects.filter(
                            user=tk.first().user).first()
        #: Set language to default language defined in settings if not settings
        #: associated with current user. It can be case if user is anonymous.
        language = usersettings.lang if usersettings else settings.LANGUAGE_CODE
        #: Notify django about updating current language.
        translation.activate(language)

        #: Update request with current language.
        request.LANGUAGE_CODE = translation.get_language()
        #: Update request with time format defined by user.
        request.TIME_FORMAT = UserSettings.TimeFormat.TWENTY_FOUR_HOUR \
            if not usersettings else usersettings.date_format

    def process_response(self, request, response):
        #: Update response headers with current language.
        language = translation.get_language()
        if 'Content-Language' not in response:
            response['Content-Language'] = language

        return response
