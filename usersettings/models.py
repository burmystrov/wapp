# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class UserSettings(models.Model):
    class TimeFormat(object):
        TWELVE_HOUR = 12
        TWENTY_FOUR_HOUR = 24
        CHOICES = (
            (TWELVE_HOUR, _('12 hour format'),),
            (TWENTY_FOUR_HOUR, _('24 hour format'),)
        )
        #: Format strings for use in `strftime`. For more information about
        #: formatting follow link:
        #: https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
        AVAILABLE_FORMATS = {
            TWENTY_FOUR_HOUR: '%H:%M:%S',
            TWELVE_HOUR: '%I:%M:%S %p',
        }

        @classmethod
        def get_format_str(cls, time_format):
            """Get format string for `strftime` depending on `time_format`
            parameter.

            :rtype: str
            """
            return cls.AVAILABLE_FORMATS.get(time_format, '')

    # time format 12 or 24 hour
    date_format = models.SmallIntegerField(
        _('Time format'), choices=TimeFormat.CHOICES,
        default=TimeFormat.TWENTY_FOUR_HOUR)
    # language code 'en' or 'ru'
    lang = models.CharField(
        _('Language code'), max_length=2, choices=settings.LANGUAGES,
        default=settings.DEFAULT_LANGUAGE)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='user_settings',
        primary_key=True
    )

    def __str__(self):
        return 'User ID #{}'.format(self.pk)

    class Meta:
        verbose_name = _('User settings')
