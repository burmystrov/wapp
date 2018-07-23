# encoding: utf-8
from __future__ import unicode_literals

from rest_framework.routers import SimpleRouter

from .views import PurchasesViewSet

router = SimpleRouter(trailing_slash=False)
router.register('purchases', PurchasesViewSet, base_name='purchases')

urlpatterns = router.urls
