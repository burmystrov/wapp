# encoding: utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_auth import urls as rest_auth_urls
from accounts.views import PasswordResetView

from common.views import api_root

#: Remove unused routes
disallowed = ['rest_login', 'rest_logout', 'rest_user_details']
rest_auth_urls.urlpatterns = list(filter(
    lambda pattern: pattern.name not in disallowed, rest_auth_urls.urlpatterns))

urlpatterns = [
    # Examples:
    url(r'^$', api_root, name='api_url'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/car/', include('typecars.urls')),
    url(r'^api/purchases/', include('purchase.urls')),
    url(r'^api/user/', include('accounts.urls')),
    url(r'^api/triggers/', include('triggers.urls')),
    url(r'^api/user/', include('consumables.urls')),
    url(r'^api/user/', include('maintenances.urls')),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(
        r'^api-auth/password/reset/$',
        PasswordResetView.as_view(), name='rest_password_reset'
    ),
    url(r'^api-auth/', include(rest_auth_urls)),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
