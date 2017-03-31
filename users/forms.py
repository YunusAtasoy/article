from django import forms
from django.db import models
from django.utils.html import format_html
from django.contrib.auth.forms import UserChangeForm as _UserChangeForm
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.db.models import Q


# Local Django
from .models import User, Activation
from magazines.models import Article
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
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = ('user_types', 'email', 'first_name',
                  'last_name', 'password1', 'password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        register = super(UserRegisterForm, self).save(commit=False)
        register.set_password(self.cleaned_data["password1"])

        if commit:
            try:
                register = User(
                    user_types=self.cleaned_data.get('user_types'),
                    email=self.cleaned_data.get('email'),
                    first_name=self.cleaned_data.get('first_name'),
                    last_name=self.cleaned_data.get('last_name'),
                    password=self.cleaned_data.get('password1'),
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


class PostForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['headline', 'text', 'subjects', 'numbers', 'pub_date']


class PasswordResetRequestForm(forms.Form):
    email_or_username = forms.CharField(label=("Email Or Username"), max_length=254)
