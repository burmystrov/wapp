# encoding: utf-8
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import User


class SwapUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data['username']
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class SwapUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
