from django.db import models
from users.models import Subject
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

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
    text = models.FileField()
    subject = models.ManyToManyField(verbose_name='Subject',
                                     to = 'users.Subject')
    pub_date = models.DateTimeField(default=timezone.now)
    confırm_types = models.PositiveSmallIntegerField(verbose_name=_('CONFIRM_TYPE'),
                                                     default=WAITING,
                                                     choices=CONFIRM_TYPES)
    user = models.ManyToManyField(verbose_name='User',
                                     to = 'users.User')
    number = models.ManyToManyField(Number, verbose_name='Number')

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.headline

    def subjects(self):
        return self.subject.get(pk=self.pk)

    def user_name(self):
        return self.user.get(pk=self.pk)

    def numbers(self):
        return self.number.get(pk=self.pk)


class Magazine(models.Model):
    magazine_name = models.CharField(max_length=100)
    publisher = models.ManyToManyField(Publisher, verbose_name='Publisher')
    number = models.ForeignKey(Number, verbose_name='Number')
    pub_date = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Magazine'
        verbose_name_plural = 'Magazines'

    def __str__(self):
        return self.magazine_name

    def publisher_name(self):
        return self.publisher.get(pk=self.pk)
