# encoding: utf-8
from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel


class StatAddress(TimeStampedModel):
    user = models.ForeignKey('accounts.User')
    address = models.CharField(max_length=255)
