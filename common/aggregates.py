# encoding: utf-8
from __future__ import unicode_literals

from django.db.models import fields
from django.db.models.expressions import Func


class Age(Func):
    function = 'AGE'
    name = 'Age'
    template = 'EXTRACT(year from %(function)s(%(expressions)s))'
    output_field = fields.IntegerField()
