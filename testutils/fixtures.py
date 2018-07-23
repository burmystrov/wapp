# encoding: utf-8
from __future__ import unicode_literals

from exam import fixture

from accounts.factories import ProfileFactory, UserFactory
from consumables.factories import (ConsumablesCategoriesFactory,
                                   ConsumablesFactory)
from guidelines.factories import GuidelinesFactory
from maintenances.factories import (AdditionalMaintenancesFactory,
                                    MaintenancesFactory)
from notifications.factories import (APNSDeviceFactory, GCMDeviceFactory,
                                     NotificationOptionsFactory)
from notifications.models import NotificationOptions
from typecars.factories import BrandsFactory, ModelsFactory
from usercars.factories import LocationImagesFactory, UserCarsFactory


class Fixtures(object):
    @fixture
    def additional_maintenance(self):
        return AdditionalMaintenancesFactory(am=self.maintenance)

    @fixture
    def admin(self):
        return self.create_user(is_superuser=True, is_staff=True)

    @fixture
    def admin_car(self):
        return UserCarsFactory(model=self.model, user=self.admin)

    @fixture
    def admin_profile(self):
        return self.admin.profile

    @fixture
    def android_device(self):
        return GCMDeviceFactory(user=self.user, active=True)

    @fixture
    def brand(self):
        return BrandsFactory(is_active=True)

    @fixture
    def consumable(self):
        return ConsumablesFactory(is_active=True, user_car=self.user_car)

    @fixture
    def consumable_category(self):
        return ConsumablesCategoriesFactory(is_active=True, user=self.user)

    def create_user(self, **kwargs):
        kwargs.setdefault('is_superuser', False)
        user = UserFactory(**kwargs)
        user.profile = ProfileFactory(user=user)
        return user

    @fixture
    def guideline(self):
        return GuidelinesFactory()

    @fixture
    def ios_device(self):
        return APNSDeviceFactory(user=self.user, active=True)

    @fixture
    def maintenance(self):
        return MaintenancesFactory(user_car=self.user_car)

    @fixture
    def model(self):
        return ModelsFactory(is_active=True, brand=self.brand)

    @fixture
    def notification_option_mileage(self):
        return NotificationOptionsFactory(
            name=NotificationOptions.Names.MILEAGE, user=self.user)

    @fixture
    def notification_option_maintenance1(self):
        return NotificationOptionsFactory(
            name=NotificationOptions.Names.MAINTENANCE1, user=self.user)

    @fixture
    def notification_option_maintenance2(self):
        return NotificationOptionsFactory(
            name=NotificationOptions.Names.MAINTENANCE2, user=self.user)

    @fixture
    def paid_user(self):
        return self.create_user(is_paid=True)

    @fixture
    def paid_user_car(self):
        return UserCarsFactory(model=self.model, user=self.paid_user)

    @fixture
    def set_notification_options(self):
        return (self.notification_option_mileage,
                self.notification_option_maintenance1,
                self.notification_option_maintenance2)

    @fixture
    def user(self):
        return self.create_user()

    @fixture
    def user_car(self):
        return UserCarsFactory(model=self.model, user=self.user)

    @fixture
    def user_car_loc_image(self):
        return LocationImagesFactory(user_car=self.user_car)

    @fixture
    def user_profile(self):
        return self.user.profile
