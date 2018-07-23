# encoding: utf-8
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils.functional import cached_property


class Helpers(object):
    view_name = None

    def check_declared_view_name(self):
        assert self.view_name is not None, (
            'Set view_name attribute in class {0}'.format(
                self.__class__.__name__
            )
        )

    @cached_property
    def list_url(self):
        self.check_declared_view_name()
        return reverse('{0}-list'.format(self.view_name))

    def detail_url(self, idx):
        self.check_declared_view_name()
        return reverse('{0}-detail'.format(self.view_name), kwargs={'pk': idx})

    def request(self, user, url, method='GET', payload=None):
        self.client.force_authenticate(user=user)
        return getattr(self.client, method.lower())(url, data=payload)

    @staticmethod
    def serialize_model(serializer, instance, request=None, many=False):
        cntx = {'request': request} if request else None
        return serializer(instance, context=cntx, many=many).data


class ExpectedFields(object):

    def __init__(self, fields):
        self.fields = set(fields)
        self.nested_objects = {}

    def add_nested(self, name, nested_object):
        assert isinstance(nested_object, ExpectedFields), (
            'nested_object param must have ExpectedFields type'
        )
        self.fields.add(name)
        self.nested_objects[name] = nested_object

    def remove_nested(self, name):
        if name in self.fields:
            self.fields.remove(name)

    def is_valid(self, data):
        assert isinstance(data, dict), 'data param must have dict type'

        if set(data.keys()) == self.fields:
            for k, v in self.nested_objects.iteritems():
                if set(data[k].keys()) == v.fields:
                    continue
                else:
                    return False
            return True
        return False
