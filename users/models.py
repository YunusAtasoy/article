# Django
from django.contrib.auth.models import Group
from django.db import models
from django.conf import settings
from django.contrib.auth.models import ( BaseUserManager,
                                         AbstractBaseUser,
                                         PermissionsMixin)
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string

# Local Django

from .variables import (
        USER_AUTHOR, USER_MANAGER,
        USER_EDITOR, USER_TYPES
)
from .variables import (
    GROUP_AUTHOR, GROUP_MANAGER, GROUP_EDITOR
)


class Subject(models.Model):
    subject = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.subject


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError(_('Users must have email address.'))

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password):
        if not email:
            raise ValueError(_('Admins must have email address.'))

        user = self.create_user(email,
            first_name=first_name,
            last_name=last_name)

        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_types = models.PositiveSmallIntegerField(
                    verbose_name=_('User'),
                    default=USER_AUTHOR,
                    choices=USER_TYPES)
    email = models.EmailField(
                    verbose_name=_('Email'),
                    max_length=255, unique=True)
    first_name = models.CharField(verbose_name=_('First Name'), max_length=50)
    last_name = models.CharField(verbose_name=_('Last Name'), max_length=50)
    is_active = models.BooleanField(verbose_name=_('Active'), default=False)
    is_staff = models.BooleanField(verbose_name=_('Staff'), default=False)
    is_developer = models.BooleanField(verbose_name=_('Developer'), default=False)
    subject = models.ManyToManyField(Subject,verbose_name='Subject')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def save(self, *args, **kwargs):
        obj = super(User, self).save(*args, **kwargs)
        try:
            if USER_AUTHOR == self.user_types :
                group = Group.objects.get(name=GROUP_AUTHOR)
                group.user_set.add(self)

            elif USER_MANAGER == self.user_types :
                group = Group.objects.get(name=GROUP_MANAGER)
                group.user_set.add(self)

            elif USER_EDITOR == self.user_types :
                group = Group.objects.get(name=GROUP_EDITOR)
                group.user_set.add(self)

        except Group.DoesNotExist:
            pass

        return super(User, self).save(*args, **kwargs)


    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)

        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_full_name()

    def get_user_type(self):
        return USER_TYPES[self.user_types][1]

    def subjects(self):
        return self.subject.get(pk=self.pk)


class Activation(models.Model):
    user = models.OneToOneField(verbose_name='User',
                              to=settings.AUTH_USER_MODEL)
    key = models.CharField(max_length=50)


    class Meta:
        verbose_name='Activation'
        verbose_name_plural='Activations'

    def __str__(self):
        return self.key

    def get_username(self):
        return self.user
