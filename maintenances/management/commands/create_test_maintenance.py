# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from django.core.management.base import BaseCommand
from accounts.models import User
from maintenances.factories import MaintenancesFactory

from typecars.factories import ModelsFactory, BrandsFactory
from typecars.models import Brands, Models
from usercars.factories import UserCarsFactory
from usercars.models import UserCars


class Command(BaseCommand):
    help = 'Create maintenance object for user with specified id.'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int)

    def handle(self, *args, **options):
        user_id = options.get('user_id')
        user = User.objects.get(id=user_id)
        brand = Brands.objects.first() or BrandsFactory()
        model = Models.objects.first() or ModelsFactory(brand=brand)
        user_car = UserCars.objects.filter(user=user).first() or \
            UserCarsFactory(user=user, model=model)
        MaintenancesFactory(user_car=user_car)
