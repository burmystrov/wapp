# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

import datetime

from common.utils import date_now


class ParamsForNextMaintenances(object):
    def __init__(self, user_car):
        self.user_car = user_car

    def service_interval_by_mileage(self):
        if self.user_car.frequency_run:
            frequency_run = self.user_car.frequency_run
        else:
            frequency_run = self.user_car.model.frequency_run
        return frequency_run * 1000

    def service_interval_by_period(self):
        return self.user_car.date_next_to * 365

    def average_daily_mileage(self):
        days = (self.current_date() - self.last_service_date()).days
        days = days if days > 0 else 1
        return (self.current_mileage() - self.last_service_mileage()) / days

    def current_mileage(self):
        return self.user_car.current_mileage

    def current_date(self):
        return date_now().date()

    def last_service_date(self):
        return self.user_car.last_service_date \
            if self.user_car.last_service_date else self.current_date()

    def last_service_mileage(self):
        return self.user_car.last_service_mileage \
            if self.user_car.last_service_mileage else self.current_mileage()

    def next_maintenace_event_by_mileage(self):
        avg = self.average_daily_mileage()
        avg = avg if avg > 0 else 1
        days = int(self.service_interval_by_mileage() / avg)
        td = datetime.timedelta(days=days)
        return (self.last_service_date() + td)

    def next_maintenance_event_by_date(self):
        return self.last_service_date() + datetime.timedelta(
            days=self.service_interval_by_period())

    def optimum_maintenance_event_date(self):
        if self.next_maintenace_event_by_mileage() > \
                self.next_maintenance_event_by_date():
            return self.next_maintenance_event_by_date()
        else:
            return self.next_maintenace_event_by_mileage()
