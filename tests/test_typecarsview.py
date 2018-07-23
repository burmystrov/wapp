# encoding: utf-8
from __future__ import unicode_literals

import urllib

from django.db.models import Count

from testutils import APITestCase, PermissionTestCase
from testutils.helpers import ExpectedFields
from typecars.factories import BrandsFactory, ModelsFactory
from typecars.models import Brands, Models
from typecars.serializers import (AdminBrandSerializer, AdminModelSerializer,
                                  BrandSerializer, ModelSerializer)


class BModelViewMixin(APITestCase):
    class_model = None
    serializer = None
    admin_serializer = None
    filters_map = None
    fields = None
    fields_admin = None
    count_field = None

    def expected_out(self, user, filters, ordering, resp):
        qs = self.class_model.objects.filter(is_active=True, **filters)
        if user.is_superuser:
            qs = qs.annotate(count=Count(self.count_field))
            serializer = self.admin_serializer
            fields = self.fields_admin
        else:
            serializer = self.serializer
            fields = self.fields
        qs = qs.order_by(ordering, '-id') if ordering else qs.order_by('-id')

        expected_out = self.serialize_model(serializer, qs, resp.wsgi_request,
                                            many=True)
        assert self.expected_fields(fields).is_valid(expected_out[0])
        return expected_out

    def assert_list(self, user, url=None, filters=None, ordering=None,
                    supports_methods=None):
        """
        :param url: for list not define
        """

        if filters is None:
            filters = {}

        # Forming url and filters for list
        if url is None:
            get_params = filters.copy()
            if ordering:
                get_params['ordering'] = ordering
            url = '{}?{}'.format(
                self.list_url, urllib.urlencode(get_params)
            ) if get_params else self.list_url

            filters = {self.filters_map[k]: v for k, v in filters.items()}

        resp = self.request(user, url)

        expected_out = self.expected_out(user, filters, ordering, resp)

        if 'results' in resp.data:
            # verify list
            for i, item in enumerate(resp.data['results']):
                self.assertDictEqual(expected_out[i], item)
        else:
            # verify detail
            self.assertDictEqual(expected_out[0], resp.data)

        if supports_methods:
            self.assert_supports_methods(resp, supports_methods)


class BModelsPermissionTestCase(object):

    def test_authentication(self):
        # Ensure it requires authentication to access to resource
        self.assert_requires_authentication(self.list_url)
        self.assert_requires_authentication(self.detail_url(self.id_detail))

    def test_access(self):
        self.assert_anonym_cannot_access(self.list_url)
        self.assert_admin_can_access(self.list_url)
        self.assert_user_can_access(self.list_url)

        detail = self.detail_url(self.id_detail)
        self.assert_anonym_cannot_access(detail)
        self.assert_user_can_access(detail)
        self.assert_admin_can_access(detail)


class BrandsPermissionTestCase(BModelsPermissionTestCase,
                               PermissionTestCase):
    view_name = 'brands'

    def setUp(self):
        self.id_detail = self.brand.id


class BrandViewTestCase(BModelViewMixin):
    class_model = Brands
    serializer = BrandSerializer
    admin_serializer = AdminBrandSerializer
    view_name = 'brands'
    filters_map = {
        'name': 'name',
    }
    fields = ('id', 'name', 'image')
    fields_admin = ('id', 'name', 'image', 'count')
    count_field = 'brand_models__model_cars'

    def expected_fields(self, fields):
        return ExpectedFields(fields)

    def setUp(self):
        BrandsFactory(is_active=True, image=None)
        self.brand_not_active = BrandsFactory(is_active=False, image=None)
        # creating usercar instance
        self.user_car

    def test_list(self):
        # All brands for non-superuser
        self.assert_list(user=self.user)

        # All brands for superuser
        self.assert_list(user=self.admin)

        # filters
        self.assert_list(user=self.user,
                         filters={'name': self.brand.name})
        self.assert_list(user=self.admin,
                         filters={'name': self.brand.name})

        # for admin order_by count
        self.assert_list(user=self.admin, ordering='count')

    def test_detail(self):
        # active element for non-admin
        detail = self.detail_url(self.brand.id)

        self.assert_list(user=self.user,
                         url=detail,
                         filters={'id': self.brand.id},
                         supports_methods='GET, HEAD, OPTIONS')

        # active element for admin
        self.assert_list(user=self.admin,
                         url=detail,
                         filters={'id': self.brand.id},
                         supports_methods='GET, HEAD, OPTIONS')

        # non-active element
        url = self.detail_url(self.brand_not_active.id)
        self.assert_not_found(self.user, url)

        # not exists element
        url = self.detail_url(0)
        self.assert_not_found(self.user, url)


class ModelsPermissionTestCase(BModelsPermissionTestCase,
                               PermissionTestCase):
    view_name = 'models'

    def setUp(self):
        self.id_detail = self.model.id


class ModelsViewTestCase(BModelViewMixin):
    class_model = Models
    serializer = ModelSerializer
    admin_serializer = AdminModelSerializer
    view_name = 'models'
    filters_map = {
        'name': 'name',
        'brand__name': 'brand__name'
    }
    fields = ('id', 'name', 'image')
    fields_admin = ('id', 'name', 'image', 'count')
    count_field = 'model_cars'

    def expected_fields(self, fields):
        expected_fields = ExpectedFields(fields)
        expected_fields.add_nested('brand', ExpectedFields((
            'id', 'name', 'image')
        ))
        return expected_fields

    def setUp(self):
        ModelsFactory.create_batch(size=1, is_active=True, image=None)
        self.model_not_active = ModelsFactory(brand=self.brand, is_active=False)
        # creating usercar instance
        self.user_car

    def test_list(self):
        # All models for non-superuser
        self.assert_list(user=self.user)

        # All models for superuser
        self.assert_list(user=self.admin)

        # filters
        self.assert_list(user=self.user,
                         filters={'name': self.model.name})
        self.assert_list(user=self.admin,
                         filters={'name': self.model.name})
        self.assert_list(user=self.user,
                         filters={'brand__name': self.brand.name})
        self.assert_list(user=self.admin,
                         filters={'brand__name': self.brand.name})

        # for admin order_by count
        self.assert_list(user=self.admin, ordering='count')

    def test_detail(self):
        # active element for non-admin
        detail = self.detail_url(self.model.id)

        self.assert_list(user=self.user,
                         url=detail,
                         filters={'id': self.model.id},
                         supports_methods='GET, HEAD, OPTIONS')

        # active element for admin
        self.assert_list(user=self.admin,
                         url=detail,
                         filters={'id': self.model.id},
                         supports_methods='GET, HEAD, OPTIONS')

        # non-active element
        url = self.detail_url(self.model_not_active.id)
        self.assert_not_found(self.user, url)

        # not exists element
        url = self.detail_url(0)
        self.assert_not_found(self.user, url)
