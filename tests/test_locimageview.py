from __future__ import unicode_literals

from functools import partial

from exam import fixture
from rest_framework import status

from testutils import APITestCase, PermissionTestCase
from testutils.helpers import ExpectedFields
from usercars.models import LocationImages
from usercars.serializers import LocationImageSerializer

image = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='


class LocImageMixin(object):
    view_name = 'location-images'
    serializer = LocationImageSerializer

    @fixture
    def expected_fields(self):
        return ExpectedFields(
            ('id', 'name', 'image', 'user_car', 'lat', 'long', 'is_main')
        )


class LocImagePermissionTestCase(LocImageMixin, PermissionTestCase):
    def test_authentication(self):
        self.assert_requires_authentication(self.list_url)
        self.assert_requires_authentication(
            self.detail_url(self.user_car_loc_image.id)
        )

    def test_access(self):
        self.assert_anonym_cannot_access(self.list_url)
        self.assert_user_can_access(self.list_url)

        detail = self.detail_url(self.user_car_loc_image.id)
        self.assert_anonym_cannot_access(detail)
        self.assert_admin_cannot_access(detail)
        self.assert_user_can_access(detail)


class LocImageViewTestCase(LocImageMixin, APITestCase):
    def setUp(self):
        # Creating instance
        self.user_car_loc_image

    def test_list(self):
        # Ensure user can see its own item
        self.assert_list(self.user, (self.user_car_loc_image,),
                         support_methods='GET, POST, HEAD, OPTIONS')

    def test_detail(self):
        detail_url = self.detail_url(self.user_car_loc_image.id)
        self.assert_detail(self.user, detail_url, self.user_car_loc_image)

    def test_update(self):
        # Ensure user can update its own item
        detail = self.detail_url(self.user_car_loc_image.id)
        payload = {'name': '~supername-123~', 'id': self.user_car_loc_image.id}
        assert self.user_car_loc_image.name != payload['name']
        resp = self.request(self.user, detail, 'PATCH', payload)
        assert resp.status_code == status.HTTP_200_OK, resp.content
        assert LocationImages.objects.filter(**payload).exists()


class CreateLocImageTestCase(LocImageMixin, APITestCase):
    def setUp(self):
        # Creating instance
        self.user_car

    @fixture
    def payload(self):
        return {'name': 'test', 'image': image, 'user_car': self.user_car.id}

    def test_create(self):
        error = 'Unable to add this image due to exceeding limit for your plan'

        partial_assert = partial(
            self.assert_plan_limit, self.list_url, self.expected_fields, error
        )

        partial_assert(
            self.payload, self.user, self.user.plan_limit('USER_IMAGES')
        )

        payload = self.payload.copy()
        payload['user_car'] = self.paid_user_car.id

        partial_assert(
            payload, self.paid_user, self.paid_user.plan_limit('USER_IMAGES')
        )

    def test_foreign_car(self):
        # Ensure user can only add image to his/her car
        resp = self.request(self.paid_user, self.list_url, 'POST', self.payload)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST, resp.content
        assert resp.data == {'user_car': ['You can only add image to your car']}
