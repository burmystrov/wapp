# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from exam import fixture
from rest_framework import status

from accounts.factories import UserFactory
from maintenances.factories import MaintenancesFactory
from maintenances.models import Maintenances
from maintenances.serializers import MaintenancesSerializer
from testutils import PermissionTestCase
from testutils.helpers import ExpectedFields
from usercars.factories import UserCarsFactory


class MaintenancesMixin(object):
    serializer = MaintenancesSerializer
    supported_list_methods = 'GET, POST, HEAD, OPTIONS'
    supported_detail_methods = 'GET, PUT, PATCH, DELETE, HEAD, OPTIONS'
    view_name = 'maintenances'

    payload = {
        'user_car': 1,
        'name': 'Engine Oil Change',
        'datetime': '2015-03-23T06:00:00',
        'mileage_to': 2010000,
        'type': 'Scheduled',
        'description': 'description'
    }

    def setUp(self):
        self.user = UserFactory()
        self.user_car = UserCarsFactory(user=self.user)
        self.payload['user_car'] = self.user_car.id
        self.maintenance = MaintenancesFactory(user_car=self.user_car)
        self.stranger = UserFactory()

    @fixture
    def expected_fields(self):
        return ExpectedFields([
            'id', 'user_car', 'name', 'datetime', 'mileage_to', 'type',
            'description'
        ])

    @fixture
    def validation_errors(self):
        return {
            'user_car': ['This field may not be blank.'],
            'name': ['This field may not be blank.'],
            'datetime': ['This field may not be blank.'],
            'mileage_to': ['This field may not be blank.'],
            'type': ['This field may not be blank.']
        }


class MaintenancesDetails(MaintenancesMixin,
                          PermissionTestCase):
    def _test_delete(self, user=None, response_status=None):
        user = user or self.user
        response_status = response_status or status.HTTP_204_NO_CONTENT
        response = self.request(user,
                                self.detail_url(self.maintenance.id),
                                method='DELETE')
        assert response.status_code == response_status, response.content

    def _test_update(self, user=None, maintenance=None, payload=None,
                     response_status=None, anonymous=False):
        maintenance = maintenance or self.maintenance
        detail_url = self.detail_url(maintenance.id)
        payload = payload or self.payload
        response_status = response_status or status.HTTP_200_OK
        user = user or self.user if not anonymous else None

        response = self.request(
            user, detail_url, method='PATCH', payload=payload)
        assert response.status_code == response_status, response.content

    def test_get_by_stranger(self):
        detail_url = self.detail_url(self.maintenance.id)
        response = self.request(self.stranger, detail_url)
        assert status.is_client_error(response.status_code), response.content

    def test_update_by_anonymous(self):
        self._test_update(anonymous=True,
                          response_status=status.HTTP_401_UNAUTHORIZED)

    def test_update_by_owner(self):
        self._test_update()

    def test_update_by_stranger(self):
        self._test_update(self.stranger,
                          response_status=status.HTTP_404_NOT_FOUND)

    def test_update_with_blank_keys(self):
        for key in self.validation_errors:
            missed = dict(self.payload)
            missed[key] = ''
            self._test_update(payload=missed,
                              response_status=status.HTTP_400_BAD_REQUEST)

    def test_delete(self):
        self._test_delete()

    def test_delete_by_stranger(self):
        self._test_delete(self.stranger, status.HTTP_404_NOT_FOUND)


class MaintenancesList(MaintenancesMixin,
                       PermissionTestCase):
    def _test_creating(self, user=None, payload=None, response_status=None,
                       anonymous=None):
        user = user or self.user if not anonymous else None
        payload = payload or self.payload
        response_status = response_status or status.HTTP_201_CREATED
        response = self.request(user, self.list_url, method='POST',
                                payload=payload)
        assert response.status_code == response_status, response.content

    def test_creating(self):
        count = Maintenances.objects.count()
        self._test_creating()
        assert Maintenances.objects.count() == count + 1

        for key in self.validation_errors:
            missed = dict(self.payload)
            missed[key] = ''
            self._test_creating(payload=missed,
                                response_status=status.HTTP_400_BAD_REQUEST)

        self._test_creating(anonymous=True,
                            response_status=status.HTTP_401_UNAUTHORIZED)
