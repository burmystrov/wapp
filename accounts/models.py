# encoding: utf-8
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from model_utils.models import TimeStampedModel
from rest_framework.authtoken.models import Token

from common.models import LocationMixin
from geo_info.models import City, Country
from notifications.models import NotificationOptions
from usersettings.models import UserSettings

logger = logging.getLogger(__name__)


class UserManager(DjangoUserManager):
    def create_user(self, username, email, password, fullname, sex, date_birth,
                    city=None, image=None, lat=None, long=None, **kwargs):
        """
        Creates an account along with profile and other related model
        instances.
        You should use this method in any case when you have to create user
        instance to be sure that it has all related data.
        """
        from statistics.models import StatAddress
        from geopy.exc import GeopyError
        from geopy.geocoders import Nominatim

        user = self._create_user(username, email, password, False, False)
        data = {
            'user': user, 'fullname': fullname, 'sex': sex, 'city': city,
            'date_birth': date_birth
        }
        if image:
            data['image'] = image
        if lat and long:
            data.update({'lat': lat, 'long': long})
            location = Nominatim()
            query = '{}, {}'.format(lat, long)
            try:
                address = location.reverse(query).address
            except GeopyError:
                address = None
                logging.error(
                    'Unable to retrieve address for user #{0} with such'
                    ' coordinates: {1}'.format(user.id, query)
                )

            if address:
                StatAddress.objects.create(user=user, address=address)
        Token.objects.create(user=user)
        Profile.objects.create(**data)
        UserSettings.objects.create(user=user)
        NotificationOptions.create_default_notification_options(user=user)
        return user


class User(AbstractUser):
    is_paid = models.BooleanField(default=False)

    objects = UserManager()

    def plan_limit(self, name):
        """Returns limit for specific type."""
        def limit(plan):
            return getattr(settings, '{}_{}'.format(name, plan))
        return limit('PAID') if self.is_paid else limit('FREE')

    def is_able_to_add_car(self):
        """Checks if user's able to add a car."""
        return self.user_cars.all().count() < self.plan_limit('USER_CARS')

    def is_able_to_add_image(self, car_id):
        """Checks if user can add image to a car."""
        from usercars.models import LocationImages

        qs = LocationImages.objects.filter(user_car_id=car_id)
        return qs.count() < self.plan_limit('USER_IMAGES')


@python_2_unicode_compatible
class Profile(LocationMixin):
    # According to ISO/IEC 5218(http://en.wikipedia.org/wiki/ISO/IEC_5218)
    NOT_KNOWN = 0
    MALE = 1
    FEMALE = 2

    SEXES = (
        (MALE, _('Male')),
        (FEMALE, _('Female'))
    )

    user = models.OneToOneField(User, related_name='profile', primary_key=True)
    fullname = models.CharField(max_length=128)
    sex = models.SmallIntegerField(choices=SEXES)
    date_birth = models.DateField()
    country = models.ForeignKey(
        Country, null=True, blank=True, related_name='user_countries'
    )
    city = models.ForeignKey(
        City, null=True, blank=True, related_name='user_cities'
    )
    image = models.ImageField(upload_to='profile', blank=True)

    @staticmethod
    def get_sex_name_by_id(sex_id):
        """Gets sex from the list by ID"""
        return next((val for idx, val in Profile.SEXES if idx == sex_id), None)

    @staticmethod
    def get_sex_id_by_name(name):
        for idx, val in Profile.SEXES:
            if val == name:
                return idx

    def __str__(self):
        return self.fullname


class OAuthAccount(TimeStampedModel):
    FACEBOOK = 'facebook'
    GOOGLE = 'google'

    PROVIDES = (
        (FACEBOOK, _('Facebook')),
        (GOOGLE, _('Google'))
    )

    user = models.ForeignKey(User, related_name='social_accounts')
    provider = models.CharField(max_length=15, choices=PROVIDES)
    uid = models.CharField(max_length=255)

    class Meta:
        unique_together = ('provider', 'uid')


@receiver(pre_save, sender=Profile, dispatch_uid='update_profile')
def update_profile(sender, instance, *args, **kwargs):
    if instance.city:
        instance.country_id = instance.city.country_id
