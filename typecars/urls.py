# encoding: utf-8
from __future__ import unicode_literals

from rest_framework.routers import SimpleRouter

from .views import BrandsView, ModelsView

router = SimpleRouter(trailing_slash=False)
router.register('brands', BrandsView, base_name='brands')
router.register('models', ModelsView, base_name='models')

urlpatterns = router.urls
