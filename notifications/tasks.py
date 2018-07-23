# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from celery.task.base import task

from usercars.models import UserCars

from .utils import send_push_notification


@task
def send_push_notifications():
    for car in UserCars.objects.select_related():
        send_push_notification(car)
