# encoding: utf-8
from __future__ import unicode_literals


class ICountry(object):
    """Country field indexes in GeoNames."""
    CODE = 0
    CODE3 = 1
    CODE_NUM = 2
    FIPS = 3
    NAME = 4
    CAPITAL = 5
    AREA = 6
    POPULATION = 7
    CONTINENT = 8
    TLD = 9
    CURRENCY_CODE = 10
    CURRENCY_NAME = 11
    PHONE = 12
    POSTAL_CODE_FORMAT = 13
    POSTAL_CODE_REGEX = 14
    LANGUAGES = 15
    GEO_NAME_ID = 16
    NEIGHBOURS = 17
    EQUIVALENT_FIPS = 18


class IRegion(object):
    """Region field indexes in GeoNames."""
    CODE = 0
    NAME = 1
    ASCII_NAME = 2
    GEO_NAME_ID = 3


class ICity(object):
    """City field indexes in GeoNames.
    Description of fields: http://download.geonames.org/export/dump/readme.txt
    """
    GEO_NAME_ID = 0
    NAME = 1
    ASCII_NAME = 2
    ALTERNATE_NAMES = 3
    LATITUDE = 4
    LONGITUDE = 5
    FEATURE_CLASS = 6
    FEATURE_CODE = 7
    COUNTRY_CODE = 8
    CC2 = 9
    ADMIN1_CODE = 10
    ADMIN2_CODE = 11
    ADMIN3_CODE = 12
    ADMIN4_CODE = 13
    POPULATION = 14
    ELEVATION = 15
    GTOPO30 = 16
    TIMEZONE = 17
    MODIFICATION_DATE = 18


class IAlternate(object):
    """Alternate names field indexes in GeoNames.
    Description of fields: http://download.geonames.org/export/dump/readme.txt
    """
    NAME_ID = 0
    GEO_NAME_ID = 1
    LANGUAGE = 2
    NAME = 3
    IS_PREFERRED = 4
    IS_SHORT = 5
    IS_COLLOQUIAL = 6
    IS_HISTORIC = 7
