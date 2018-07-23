# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from exam import fixture
from rest_framework import status

from consumables.models import Consumables
from consumables.serializers import (ConsumablesCategoriesSerializer,
                                     ConsumablesSerializer)
from testutils import PermissionTestCase
from testutils.helpers import ExpectedFields

BASE64_IMAGE = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='


class ConsumablesCategoriesMixin(object):
    view_name = 'consumables_categories'
    serializer = ConsumablesCategoriesSerializer
    supported_list_methods = 'GET, POST, HEAD, OPTIONS'
    supported_detail_methods = 'GET, PUT, PATCH, DELETE, HEAD, OPTIONS'

    @fixture
    def expected_fields(self):
        return ExpectedFields(['id', 'name', 'is_general'])


class ConsumablesCategoriesTestView(ConsumablesCategoriesMixin,
                                    PermissionTestCase):

    def setUp(self):
        self.consumable_category

    def test_retrieving_list(self):
        self.assert_requires_authentication(self.list_url)
        self.assert_anonym_cannot_access(self.list_url)
        self.assert_user_can_access(self.list_url)

        self.assert_list(self.user, self.consumable_category,
                         support_methods=self.supported_list_methods)

    def test_get(self):
        detail_url = self.detail_url(self.consumable_category.id)
        self.assert_requires_authentication(detail_url)
        self.assert_anonym_cannot_access(detail_url)
        self.assert_user_can_access(detail_url)

        self.assert_detail(self.user, detail_url, self.consumable_category,
                           support_methods=self.supported_detail_methods)


class ConsumablesViewMixin(object):
    view_name = 'consumables'
    serializer = ConsumablesSerializer
    supported_list_methods = 'GET, POST, HEAD, OPTIONS'
    supported_detail_methods = 'GET, PUT, PATCH, DELETE, HEAD, OPTIONS'

    @fixture
    def expected_fields(self):
        return ExpectedFields(['id', 'category', 'user_car',
                               'name', 'description', 'image', 'created'])

    @fixture
    def payload(self):
        return {
            'category': self.consumable_category.id,
            'user_car': self.user_car.id,
            'name': 'Air filter',
            'image': BASE64_IMAGE
        }


class ConsumablesListView(ConsumablesViewMixin,
                          PermissionTestCase):
    def test_creating_consumables(self):
        count = Consumables.objects.count()
        response = self.request(self.user, self.list_url,
                                method='POST', payload=self.payload)
        assert response.status_code == status.HTTP_201_CREATED, response.content
        assert Consumables.objects.count() == count + 1

        errors = {
            'category': ['This field may not be blank.'],
            'user_car': ['This field may not be blank.'],
            'name': ['This field may not be blank.'],
        }
        for key in errors:
            missed = dict(self.payload)
            del missed[key]
            response = self.request(self.user, self.list_url,
                                    method='POST', payload=missed)
            assert response.status_code == status.HTTP_400_BAD_REQUEST, \
                response.content

        response = self.request(None, self.list_url,
                                method='POST', payload=self.payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            response.content

    def test_retrieving_list(self):
        self.assert_requires_authentication(self.list_url)
        self.assert_anonym_cannot_access(self.list_url)
        self.assert_user_can_access(self.list_url)

        self.assert_list(self.user, self.consumable,
                         support_methods=self.supported_list_methods)


class ConsumablesDetailView(ConsumablesViewMixin,
                            PermissionTestCase):
    def test_get(self):
        detail_url = self.detail_url(self.consumable.id)
        self.assert_requires_authentication(detail_url)
        self.assert_anonym_cannot_access(detail_url)
        self.assert_user_can_access(detail_url)

        self.assert_detail(self.user, detail_url, self.consumable,
                           support_methods=self.supported_detail_methods)

    def test_update(self):
        detail_url = self.detail_url(self.consumable.id)
        response = self.request(self.user, detail_url,
                                method='PATCH', payload=self.payload)
        assert response.status_code == status.HTTP_200_OK, \
            (response.content, detail_url)

        errors = {
            'category': ['This field may not be blank.'],
            'user_car': ['This field may not be blank.'],
            'name': ['This field may not be blank.'],
            'image': ['This field may not be blank.']
        }
        for key in errors:
            missed = dict(self.payload)
            missed[key] = ''
            response = self.request(self.user, detail_url,
                                    method='PATCH', payload=missed)
            assert response.status_code == status.HTTP_400_BAD_REQUEST, \
                response.content

        response = self.request(None, detail_url,
                                method='PATCH', payload=self.payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, \
            response.content
