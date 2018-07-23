# encoding: utf-8
from __future__ import unicode_literals

from django.core.management.base import BaseCommand

from django.conf import settings

from ...geo_names import GeoNamesData
from ...models import Country, Region, City
from ...struct import IAlternate, IRegion, ICity, ICountry


class Command(BaseCommand):
    #: Keeps all countries to avoid redundant hits to database.
    countries = {}
    #: Keeps all regions having `geoname_code`
    regions = {}

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        self.languages = [l[0] for l in settings.LANGUAGES]
        # Keeps data with translated names
        self.trans = {n: {} for n in self.languages}

    def handle(self, *args, **options):
        print('Loading translations')
        for url in settings.TRANSLATION_SOURCES:
            self.load_trans(GeoNamesData(url))

        print('Importing countries')
        self.import_data(settings.COUNTRY_SOURCES, 'country', Country)
        print('Indexing countries')
        self.index_countries()
        print('Importing regions')
        self.import_data(settings.REGION_SOURCES, 'region', Region)
        print('Indexing regions')
        self.index_regions()
        print('Importing cities')
        self.import_data(settings.CITY_SOURCES, 'city', City)

    def load_trans(self, geo_names):
        """Loads translations."""
        for item in geo_names.parse():
            lang = item.get(IAlternate.LANGUAGE)
            if lang not in self.languages:
                continue
            geo_name_id = item.get(IAlternate.GEO_NAME_ID)
            if not geo_name_id or geo_name_id in self.trans[lang]:
                continue

            name = item.get(IAlternate.NAME)
            if name:
                self.trans[lang][geo_name_id] = name

    def index_countries(self):
        """Loads all countries from database and keeps it in memory"""
        for country in Country.objects.all():
            if country.code2:
                self.countries[country.code2] = country

    def index_regions(self):
        """Loads all regions from database and keeps it in memory"""
        for region in Region.objects.all():
            if region.geoname_code:
                code2, _ = region.geoname_code.split('.')
                self.regions[_] = region

    def import_data(self, sources, name, model):
        items = []
        method = getattr(self, 'extract_{}'.format(name))
        for url in sources:
            for item in GeoNamesData(url).parse():
                result = method(item)
                if result:
                    items.append(model(**result))
        model.objects.bulk_create(items)

    def extract_city(self, item):
        geo_name_id = item.get(ICity.GEO_NAME_ID)
        code2 = item.get(ICity.COUNTRY_CODE)
        country = self.countries.get(code2)
        region = self.regions.get(item.get(ICity.CC2))

        if not geo_name_id or not country:
            return
        kwargs = {
            'geoname_id': geo_name_id,
            'country': country
        }

        if region:
            kwargs['region'] = region

        for lang in self.languages:
            trans_name = self.trans[lang].get(geo_name_id)
            if trans_name:
                kwargs['name_{}'.format(lang)] = trans_name

        default_name = 'name_{}'.format(settings.DEFAULT_LANGUAGE)
        if default_name not in kwargs:
            kwargs[default_name] = item.get(IRegion.NAME)
        return kwargs

    def extract_country(self, item):
        geo_name_id = item.get(ICountry.GEO_NAME_ID)
        if not geo_name_id:
            return

        kwargs = {
            'continent': item.get(ICountry.CONTINENT),
            'code2': item.get(ICountry.CODE),
            'code3': item.get(ICountry.CODE3),
            'geoname_id': geo_name_id
        }

        tld = item.get(ICountry.TLD)
        if tld:
            kwargs['tld'] = tld[1:]

        for lang in self.languages:
            trans_name = self.trans[lang].get(geo_name_id)
            if trans_name:
                kwargs['name_{}'.format(lang)] = trans_name
        return kwargs

    def extract_region(self, item):
        code = item.get(IRegion.CODE)
        if not code:
            return

        code2, _ = code.split('.')
        geo_name_id = item.get(IRegion.GEO_NAME_ID)
        country = self.countries.get(code2)
        if not geo_name_id or not country:
            return

        kwargs = {
            'geoname_code': code,
            'geoname_id': geo_name_id,
            'country': country
        }

        for lang in self.languages:
            trans_name = self.trans[lang].get(geo_name_id)
            if trans_name:
                kwargs['name_{}'.format(lang)] = trans_name

        default_name = 'name_{}'.format(settings.DEFAULT_LANGUAGE)
        if default_name not in kwargs:
            kwargs[default_name] = item.get(IRegion.NAME)
        return kwargs
