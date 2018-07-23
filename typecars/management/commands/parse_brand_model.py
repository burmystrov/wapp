# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

import requests

from django.core.management.base import BaseCommand

from typecars.models import Brands, Models


class Command(BaseCommand):
    brands_url = 'https://auto.ria.com/api/categories/1/marks/' \
                 '_active/_with_count?langId=4&categoryId=1'
    models_url = 'https://auto.ria.com/api/categories/1/marks/' \
                 '{}/models/_with_count?langId=4'

    def handle(self, *args, **options):
        data_json_brand = requests.get(self.brands_url)
        for brand in data_json_brand.json():
            brand_obj, created = Brands.objects.get_or_create(
                name=brand.get('name')
            )
            data_json_model  = requests.get(
                self.models_url.format(brand.get('value'))
            )
            for model in data_json_model.json():
                Models.objects.get_or_create(
                    brand=brand_obj, name=model.get('name')
                )
