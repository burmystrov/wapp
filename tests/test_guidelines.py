# ~*~ encoding: utf-8 ~*~
from __future__ import unicode_literals

from exam import fixture

from guidelines.serializers import GuidelinesSerializer
from testutils import PermissionTestCase
from testutils.helpers import ExpectedFields


class GuidelinesViewMixin(object):
    serializer = GuidelinesSerializer
    supported_list_methods = 'GET, HEAD, OPTIONS'
    supported_detail_methods = 'GET, HEAD, OPTIONS'
    view_name = 'guidelines'

    @fixture
    def expected_fields(self):
        return ExpectedFields(['id', 'name', 'file_video', ])


class TestGuidelinesListView(GuidelinesViewMixin, PermissionTestCase):
    def test_retrieving_list(self):
        self.assert_requires_authentication(self.list_url)
        self.assert_anonym_cannot_access(self.list_url)
        self.assert_user_can_access(self.list_url)

        self.assert_list(self.user, self.guideline,
                         support_methods=self.supported_list_methods)


class GuidelinesDetailView(GuidelinesViewMixin, PermissionTestCase):
    def test_get(self):
        detail_url = self.detail_url(self.guideline.id)
        self.assert_requires_authentication(detail_url)
        self.assert_anonym_cannot_access(detail_url)
        self.assert_user_can_access(detail_url)

        self.assert_detail(self.user, detail_url, self.guideline,
                           support_methods=self.supported_detail_methods)
