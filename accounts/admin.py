# encoding: utf-8
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _

from .forms import SwapUserChangeForm, SwapUserCreationForm
from .models import Profile, User


class ExtUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions', 'is_paid')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    form = SwapUserChangeForm
    add_form = SwapUserCreationForm


admin.site.register(User, ExtUserAdmin)
admin.site.register(Profile)
