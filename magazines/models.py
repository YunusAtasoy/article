# Django
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Local Django
from users.models import User, Subject
from users.variables import (
        CONFIRM, EDIT,
        WAITING, CONFIRM_TYPES
)


class Publisher(models.Model):
    publisher_name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'

    def __str__(self):
        return self.publisher_name


class Number(models.Model):
    number = models.PositiveSmallIntegerField(verbose_name='Number')
    class Meta:
        verbose_name = 'Number'
        verbose_name_plural = 'Numbers'

    def __str__(self):
        return "{a}".format(a=self.number)



class Article(models.Model):
    headline = models.CharField(max_length=50)
    text = models.TextField()
    subjects = models.ManyToManyField(verbose_name=_('Subject'),
                                     to=Subject)
    pub_date = models.DateTimeField(default=timezone.now)
    confırm_types = models.PositiveSmallIntegerField(verbose_name=_('CONFIRM_TYPE'),
                                                     default=WAITING,
                                                     choices=CONFIRM_TYPES)
    users = models.ManyToManyField(verbose_name=_('User'),
                                  to=User)
    numbers = models.ManyToManyField(Number, verbose_name='Number')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.headline

    def subject(self):
        return ", ".join([i.__str__() for i in self.subjects.all()])

    def users_name(self):
        return ", ".join([i.__str__() for i in self.users.all()])

    def number(self):
        return ", ".join([i.__str__() for i in self.numbers.all()])


class Magazine(models.Model):
    magazine_name = models.CharField(max_length=100)
    publishers = models.ManyToManyField(Publisher, verbose_name='Publisher')
    number = models.ForeignKey(Number, verbose_name='Number')
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Magazine'
        verbose_name_plural = 'Magazines'

    def __str__(self):
        return self.magazine_name

    def publisher_name(self):
        return ", ".join([i.__str__() for i in self.publishers.all()])
