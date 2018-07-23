# encoding: utf-8
from __future__ import unicode_literals

from exam import fixture
from rest_framework import status

from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from testutils import APITestCase, PermissionTestCase
from testutils.helpers import ExpectedFields


class ProfileViewMixin(object):
    view_name = 'profiles'
    serializer = ProfileSerializer

    @fixture
    def expected_fields(self):
        expected_fields = ExpectedFields(
            ('id', 'sex', 'city', 'date_birth', 'image', 'lat', 'long',
             'fullname')
        )
        expected_fields.add_nested('user', ExpectedFields((
            'id', 'username', 'is_paid', 'email')
        ))
        return expected_fields


class ProfileViewPermissionTestCase(ProfileViewMixin, PermissionTestCase):
    def test_authentication(self):
        self.assert_requires_authentication(self.list_url)
        self.assert_requires_authentication(
            self.detail_url(self.admin_profile.pk)
        )

    def test_access(self):
        self.assert_anonym_cannot_access(self.list_url)
        self.assert_admin_can_access(self.list_url)
        self.assert_user_can_access(self.list_url)

        detail = self.detail_url(self.admin_profile.pk)

        self.assert_anonym_cannot_access(detail)
        self.assert_user_cannot_access(detail)
        self.assert_admin_can_access(detail)


class ProfileViewTestCase(ProfileViewMixin, APITestCase):
    def test_update_detail(self):
        # Ensure user can update only itself
        payload = {'fullname': 'Mitchell K. Masters'}
        self.assertNotEqual(self.user_profile.fullname, payload['fullname'])

        resp = self.request(
            self.user, self.detail_url(self.user_profile.pk), 'PATCH', payload
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['fullname'], payload['fullname'])
        self.assertTrue(
            Profile.objects.filter(fullname=payload['fullname']).exists()
        )

        resp = self.request(
            self.user, self.detail_url(self.admin_profile.pk), 'PATCH', payload
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
        self.assertDictEqual(resp.data, {'detail': 'Not found.'})
