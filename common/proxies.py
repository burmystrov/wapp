# encoding: utf-8
from __future__ import unicode_literals


class ModelProxy(object):
    """
    `ModelProxy` is intended to build complex instance while creating an object
    in serializer. In case, if you need to set complex attributes that cannot be
    set via traditional way you may use `extra_build` method for this purpose.
    """

    #: Fields which are taken from model instance and set to ModelProxy
    # as attributes
    fields = None
    #: Used for getting related object's attributes
    nested_fields = None

    def __init__(self, instance):
        self.instance = instance

        assert isinstance(self.fields, (list, tuple)), (
            '`fields` property must be declared in '
            'class {0}'.format(self.__class__.__name__)
        )

        if self.nested_fields:
            assert isinstance(self.nested_fields, dict), (
                'nested_fields property must be declared in '
                'class {0} properly'.format(self.__class__.__name__)
            )

    def build(self):
        """Sets attributes of instance as though its own"""
        for field in self.fields:
            setattr(self, field, getattr(self.instance, field))

        if self.nested_fields:
            for k, fields in self.nested_fields.iteritems():
                attr = getattr(self.instance, k)
                for field in fields:
                    setattr(self, field, getattr(attr, field))
        if hasattr(self, 'extra_build') and callable(self.extra_build):
            self.extra_build()
        return self
