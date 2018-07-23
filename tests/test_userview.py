# encoding: utf-8
from __future__ import unicode_literals

from datetime import timedelta

from django.utils.timezone import now
from exam import fixture
from rest_framework import status

from accounts.serializers import UserSerializer
from testutils import APITestCase, PermissionTestCase
from testutils.helpers import ExpectedFields


class UserViewMixin(object):
    view_name = 'users'
    serializer = UserSerializer
    now = now()
    yesterday = now - timedelta(days=1)

    @fixture
    def user(self):
        return self.create_user(date_joined=self.yesterday)

    @fixture
    def expected_fields(self):
        return ExpectedFields(('id', 'username', 'is_paid', 'email'))


class UserViewPermissionTestCase(UserViewMixin, PermissionTestCase):
    def test_authentication(self):
        # Ensure it requires authentication to access to resource
        self.assert_requires_authentication(self.list_url)
        self.assert_requires_authentication(self.detail_url(self.admin.id))

    def test_access(self):
        self.assert_anonym_cannot_access(self.list_url)
        self.assert_admin_can_access(self.list_url)
        self.assert_user_can_access(self.list_url)

        detail = self.detail_url(self.admin.id)

        self.assert_anonym_cannot_access(detail)
        # Ensure user cannot access another detail resource except itself
        self.assert_user_cannot_access(detail)
        self.assert_admin_can_access(detail)


class UserViewTestCase(UserViewMixin, APITestCase):
    def test_list(self):
        # Ensure it returns all users if it's admin otherwise itself
        self.assert_list(self.user, (self.user,),
                         support_methods='GET, HEAD, OPTIONS')
        self.assert_list(self.admin, (self.user, self.admin),
                         support_methods='GET, HEAD, OPTIONS')

    def test_list_filter(self):
        yesterday_date = self.yesterday.date().isoformat()
        payload = {'date_to': yesterday_date}
        # Ensure it returns empty list if nothing is found
        self.assert_list(self.user, [], payload)

        payload = {'date_from': yesterday_date}
        # Ensure filter doesn't work if it's simple user
        self.assert_list(self.user, (self.user,), payload)

        # Ensure filter works for admin
        self.assert_list(self.admin, (self.user, self.admin), payload)

        self.assert_list(
            self.admin, (self.admin,),
            {'date_from': self.now.date().isoformat()}
        )

    def test_user_detail(self):
        # Ensure user without admin permissions cannot access any resource
        # except itself

        detail_url = self.detail_url(self.user.id)
        self.assert_detail(self.user, detail_url, self.user)

        resp = self.client.get(self.detail_url(self.admin.id))
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(resp.data, {'detail': 'Not found.'})

    def test_admin_detail(self):
        # Ensure admin user can access any existing resource
        detail_url = self.detail_url(self.user.id)
        self.assert_detail(self.admin, detail_url, self.user)
        detail_url = self.detail_url(self.admin.id)
        self.assert_detail(self.admin, detail_url, self.admin)
