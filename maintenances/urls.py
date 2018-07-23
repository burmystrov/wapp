# encoding: utf-8
from __future__ import unicode_literals

from rest_framework.routers import SimpleRouter

from .views import AdditionalMaintenancesView, MaintenancesView

router = SimpleRouter(trailing_slash=False)
router.register('maintenances', MaintenancesView, base_name='maintenances')
router.register('additional-maintenances', AdditionalMaintenancesView,
                base_name='additional_maintenances')

urlpatterns = router.urls
