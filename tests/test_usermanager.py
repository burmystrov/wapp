# encoding: utf-8
from __future__ import unicode_literals

from accounts.factories import ProfileFactory, UserFactory
from accounts.models import User
from testutils import TestCase


class UserManagerTestCase(TestCase):
    def test_create_user(self):
        # Ensure User's created along with profile
        data = ProfileFactory.attributes()
        data.update(UserFactory.attributes())

        self.assertEqual(User.objects.all().count(), 0)
        with self.assertNumQueries(7):
            User.objects.create_user(**data)

        user = User.objects.get(username=data['username'], email=data['email'])

        # attributes are set to False by default
        for attr in ['is_paid', 'is_staff', 'is_superuser']:
            self.assertFalse(getattr(user, attr))

        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password(data['password']))

        profile = user.profile
        for attr in ['fullname', 'sex', 'date_birth']:
            self.assertEqual(getattr(profile, attr), data[attr])

        # Ensure image is uploaded
        self.assertTrue(profile.image)
