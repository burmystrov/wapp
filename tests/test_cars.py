# encoding: utf-8
from __future__ import unicode_literals

from exam import fixture
from rest_framework import status

from testutils import APITestCase, PermissionTestCase
from testutils.helpers import ExpectedFields
from usercars.models import UserCars
from usercars.serializers import CarMileageSerializer, UserCarsSerializer


class UserCarsViewMixin(object):
    view_name = 'cars'
    serializer = UserCarsSerializer
    list_methods = 'GET, POST, HEAD, OPTIONS'

    @fixture
    def expected_fields(self):
        return ExpectedFields((
            'id', 'model', 'model_year', 'current_mileage', 'last_service_date',
            'last_service_mileage', 'frequency_run', 'date_next_to', 'image',
            'notifications',
        ))


class CarMileageViewMixin(object):
    view_name = 'car-mileages'
    serializer = CarMileageSerializer
    list_methods = 'GET, HEAD, OPTIONS'

    @fixture
    def expected_fields(self):
        return ExpectedFields(('id', 'current_mileage'))


class UserCarPermissionMixin(object):
    def test_authentication(self):
        self.assert_requires_authentication(self.list_url)
        self.assert_requires_authentication(self.detail_url(self.user_car.id))

    def test_access(self):
        self.assert_anonym_cannot_access(self.list_url)
        self.assert_user_can_access(self.list_url)

        detail = self.detail_url(self.user_car.id)
        self.assert_anonym_cannot_access(detail)
        self.assert_admin_cannot_access(detail)
        self.assert_user_can_access(detail)

        detail = self.detail_url(self.admin_car.id)
        self.assert_user_cannot_access(detail)
        self.assert_admin_can_access(detail)


class CarAbstractTestCase(object):
    def setUp(self):
        # Creating instances
        self.user_car
        self.admin_car


class UserCarsViewPermissionTestCase(UserCarsViewMixin,
                                     UserCarPermissionMixin,
                                     PermissionTestCase):
    pass


class CarMileageViewPermissionTestCase(CarMileageViewMixin,
                                       UserCarPermissionMixin,
                                       PermissionTestCase):
    pass


class CarMileageViewTestCase(CarMileageViewMixin,
                             CarAbstractTestCase,
                             APITestCase):
    def test_update(self):
        detail = self.detail_url(self.user_car.id)
        payload = {'current_mileage': 10000000, 'id': self.user_car.id}
        assert self.user_car.current_mileage != payload['current_mileage']

        # Attempt to update item from another user
        resp = self.request(self.admin, detail, 'PATCH', payload)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        # Ensure user can update only its own item
        resp = self.request(self.user, detail, 'PATCH', payload)
        assert resp.status_code == status.HTTP_200_OK
        assert UserCars.objects.filter(**payload).exists()


class UserCarsViewTestCase(UserCarsViewMixin,
                           CarAbstractTestCase,
                           APITestCase):
    def test_delete(self):
        detail = self.detail_url(self.admin_car.id)

        # Attempt to delete item from another user
        resp = self.request(self.user, detail, 'DELETE')
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        assert UserCars.objects.count() == 2

        # Ensure user can delete its own item
        resp = self.request(self.admin, detail, 'DELETE')
        assert resp.status_code == status.HTTP_204_NO_CONTENT

        # Ensure item has been deleted
        assert UserCars.objects.count() == 1

    def test_update(self):
        detail = self.detail_url(self.user_car.id)

        payload = {'model_year': 1801, 'id': self.user_car.id}
        assert self.user_car.model_year != payload['model_year']

        # Attempt to update item from another user
        resp = self.request(self.admin, detail, 'PATCH', payload)
        assert resp.status_code == status.HTTP_404_NOT_FOUND

        # Ensure user can update only its own item
        resp = self.request(self.user, detail, 'PATCH', payload)
        assert resp.status_code == status.HTTP_200_OK
        assert UserCars.objects.filter(**payload).exists()


class CreateUserCarsViewTestCase(UserCarsViewMixin, APITestCase):
    @fixture
    def payload(self):
        return {
            'model': self.model.id,
            'model_year': 2000,
            'current_mileage': 1000,
        }

    def test_unknown_model(self):
        # Ensure user can use only known models while creating an item
        payload = self.payload.copy()
        payload['model'] = 1000
        resp = self.request(self.user, self.list_url, 'POST', payload)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert resp.data == {
            'model': ['Invalid pk "1000" - object does not exist.']
        }
