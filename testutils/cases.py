# encoding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase as BaseAPITestCase

from .fixtures import Fixtures
from .helpers import Helpers

__all__ = ('TestCase', 'APITestCase', 'PermissionTestCase')


class APITestCase(Fixtures, Helpers, BaseAPITestCase):

    def assert_supports_methods(self, response, methods):
        # Ensure it supports only provided methods
        supported_methods = response._headers['allow'][1]
        assert supported_methods == methods, (supported_methods, methods)

    def assert_requires_authentication(self, url, method='GET'):
        resp = self.request(None, url, method)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED, resp.content

    def assert_list(self, user, out_obj, payload=None, support_methods=None):
        resp = self.request(user, self.list_url, payload=payload)
        assert resp.status_code == status.HTTP_200_OK, resp.content

        if not isinstance(out_obj, (list, tuple)):
            out_obj = (out_obj, )

        expected_out = [
            self.serialize_model(self.serializer, exp, resp.wsgi_request)
            for exp in out_obj
        ]

        # TODO: refactor
        # order of fields in `expected_out` and may not be equal
        for i, item in enumerate(resp.data['results']):
            assert self.expected_fields.is_valid(item)
            self.assertDictEqual(expected_out[i], item)

        if support_methods:
            self.assert_supports_methods(resp, support_methods)

    def assert_detail(self, user, url, out_obj, payload=None,
                      support_methods=None):
        resp = self.request(user, url, payload=payload)
        assert resp.status_code == status.HTTP_200_OK, resp.content

        expected_out = self.serialize_model(
            self.serializer, out_obj, resp.wsgi_request
        )

        assert self.expected_fields.is_valid(resp.data), resp.data
        assert expected_out == resp.data

        if support_methods:
            self.assert_supports_methods(resp, support_methods)

    def assert_plan_limit(self, url, expected_fields, error_msg, payload, user,
                          limit):
        # Ensure user cannot create more than it's allowed for his/her plan.
        for i in range(limit):
            resp = self.request(user, url, 'POST', payload)
            assert resp.status_code == status.HTTP_201_CREATED, resp.content
            assert expected_fields.is_valid(resp.data)

        resp = self.request(user, url, 'POST', payload)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST, resp.content
        assert resp.data == {'error': error_msg}, resp.data

    def assert_not_found(self, user, url):
        resp = self.request(user, url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(resp.data, {'detail': 'Not found.'})


class BaseTestCase(TestCase):
    pass


class PermissionTestCase(APITestCase):
    def assert_access(self, callback, user, url, method):
        resp = self.request(user, url, method)
        self.assertTrue(callback(resp.status_code))

    def assert_can_access(self, user=None, url=None, method='GET'):
        self.assert_access(status.is_success, user, url, method)

    def assert_cannot_access(self, user=None, url=None, method='GET'):
        self.assert_access(status.is_client_error, user, url, method)

    def assert_anonym_cannot_access(self, path):
        self.assert_cannot_access(AnonymousUser(), path)

    def assert_admin_can_access(self, path):
        self.assert_can_access(self.admin, path)

    def assert_admin_cannot_access(self, path):
        self.assert_cannot_access(self.admin, path)

    def assert_user_can_access(self, path):
        self.assert_can_access(self.user, path)

    def assert_user_cannot_access(self, path):
        self.assert_cannot_access(self.user, path)
