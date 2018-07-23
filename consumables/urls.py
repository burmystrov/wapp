# encoding: utf-8
from __future__ import unicode_literals

from rest_framework.routers import SimpleRouter

from .views import ConsumablesCategoriesView, ConsumablesView

router = SimpleRouter(trailing_slash=False)
router.register('consumables', ConsumablesView, base_name='consumables')
router.register('consumables-categories', ConsumablesCategoriesView,
                base_name='consumables_categories')

urlpatterns = router.urls
