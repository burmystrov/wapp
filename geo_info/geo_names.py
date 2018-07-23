# encoding: utf-8
from __future__ import unicode_literals

import codecs
import os
import zipfile

import six
from django.conf import settings


class Item(object):
    def __init__(self, item):
        self.item = item
        self.size = len(item)

    def get(self, index):
        if 0 <= index < self.size:
            return self.item[index]


class GeoNamesData(object):
    # Flag to turn the cache off while downloading
    skip_cache = False

    def __init__(self, url, skip_cache=None):
        if isinstance(skip_cache, bool):
            self.skip_cache = skip_cache
        self.url = url

        # Ensure there's a folder to keep the cache
        if not os.path.isdir(settings.GEO_INFO_CACHE):
            os.mkdir(settings.GEO_INFO_CACHE)

        filename = url.split('/')[-1]
        self.file_path = os.path.join(settings.GEO_INFO_CACHE, filename)

        self.download()

        if filename.endswith('.zip'):
            n_filename = filename.replace('.zip', '.txt')
            file_path = os.path.join(settings.GEO_INFO_CACHE, n_filename)
            self.unpack(n_filename, file_path)
            self.file_path = file_path

    def unpack(self, file_name, file_path):
        """Unpacks file from archive
        :param file_name: Filename in archive
        :param file_path: File path to unpacked file if it's present
        """
        if not os.path.isfile(file_path):
            zip_file = zipfile.ZipFile(self.file_path)
            if zip_file:
                zip_file.extract(file_name, settings.GEO_INFO_CACHE)

    def download(self):
        """Downloads data from remote resource or takes from cache"""
        if not (os.path.isfile(self.file_path) and not self.skip_cache):
            data_file = six.moves.urllib.request.urlopen(self.url)
            with open(self.file_path, 'wb') as fp:
                fp.write(data_file.read())

    def parse(self):
        with codecs.open(self.file_path, 'rb', 'utf-8') as fp:
            for line in fp:
                line = line.strip()
                if len(line) < 1 or line[0] == '#':
                    continue
                yield Item([e.strip() for e in line.split('\t')])
