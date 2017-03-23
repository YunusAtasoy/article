from django import forms
from django.db import models
from django.utils.html import format_html
from django.contrib.auth.forms import UserChangeForm as _UserChangeForm
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.contrib.auth import authenticate, login, logout


# Local Django
from .models import User
from .variables import (
    GROUP_AUTHOR, GROUP_MANAGER, GROUP_EDITOR
)

from .variables import (
        USER_AUTHOR, USER_MANAGER,
        USER_EDITOR, USER_TYPES
)




class CustomReadOnlyPasswordHashWidget(forms.Widget):
    def render(self, name, value, attrs):
        return format_html(_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"../password/\">this form</a>."
        ))


class CustomReadOnlyPasswordHashField(forms.Field):
    widget = CustomReadOnlyPasswordHashWidget

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('required', False)
        super(CustomReadOnlyPasswordHashField, self).__init__(*args, **kwargs)

    def bound_data(self, data, initial):
        return initial

    def has_changed(self, initial, data):
        return False


class UserChangeForm(_UserChangeForm):
    password = CustomReadOnlyPasswordHashField(
        label=_('Password'),
)


class UserRegisterForm(forms.ModelForm):
    user_types = models.PositiveSmallIntegerField(verbose_name=_('User'),
                                                  default=USER_AUTHOR,
                                                  choices=USER_TYPES)
    email = forms.EmailField(label=_('E-Mail Address'))
    first_name = forms.CharField(label=_('First Name'), max_length=100)
    last_name = forms.CharField(label=_('Last Name'), max_length=100)
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_types', 'email', 'first_name', 'last_name', 'password')

    def save(self, commit=True):
        register = super(UserRegisterForm, self).save(commit=False)

        if commit:
            try:
                register = User(
                    user_types=self.cleaned_data.get('user_types'),
                    email=self.cleaned_data.get('email'),
                    first_name=self.cleaned_data.get('first_name'),
                    last_name=self.cleaned_data.get('last_name'),
                    password=self.cleaned_data.get('password'),
                )
                register.save()
            except:
                register = None

        return register


class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password')

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user = authenticate(email=email, password=password)
        if email and password:
            if not user:
                raise forms.ValidationError("This user does not exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password.")
            if not user.is_active:
                raise forms.ValidationError("This user is not longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)
