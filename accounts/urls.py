# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from django.conf.urls import url
from rest_framework.routers import SimpleRouter

from accounts.views import (OAuthConnectView, ObtainAuthToken, ProfileView,
                            SignUpView, UserView)
from geo_info.views import CityView, CountryView
from guidelines.views import GuidelinesViewSet
from notifications.views import (NotificationOptionViewSet,
                                 RegisterAPNSDeviceViewSet,
                                 RegisterGCMDeviceViewSet)
from usercars.views import CarMileageView, LocImageViewSet, UserCarsViewSet
from usersettings.views import UserSettingsViewSet

router = SimpleRouter(trailing_slash=False)
router.register('android-devices', RegisterGCMDeviceViewSet,
                base_name='android-devices')
router.register('cars', UserCarsViewSet, base_name='cars')
router.register('car-mileages', CarMileageView, base_name='car-mileages')
router.register('cities', CityView, base_name='cities')
router.register('countries', CountryView, base_name='countries')
router.register('guidelines', GuidelinesViewSet, base_name='guidelines')
router.register('ios-devices', RegisterAPNSDeviceViewSet,
                base_name='ios-devices')
router.register('location-images',
                LocImageViewSet, base_name='location-images')
router.register('notification-options',
                NotificationOptionViewSet, base_name='notification-options')
router.register('profiles', ProfileView, base_name='profiles')
router.register('settings', UserSettingsViewSet, base_name='user-settings')
router.register('users', UserView, base_name='users')


urlpatterns = router.urls + [
    url(r'^login$', ObtainAuthToken.as_view(), name='login'),
    url(r'^oauth/(?P<provider_name>[a-z]+)$',
        OAuthConnectView.as_view(), name='oauth'),
    url(r'^registration$', SignUpView.as_view(), name='registration'),
]
