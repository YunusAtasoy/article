from django.db.models import Q
from django.contrib.auth.models import Permission, Group

# Local Django
from .variables import (
    GROUP_AUTHOR, GROUP_MANAGER, GROUP_EDITOR
)


def create_group(group_name, permissions):
    try:
        group = Group.objects.get(name=group_name)

        group.permissions.clear()
        group.permissions.add(*permissions)
    except Group.DoesNotExist:
        group = Group.objects.create(name=group_name)
        group.permissions.add(*permissions)

def author_group():
    user_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['users'])
            & Q(codename__icontains='User'))]

    magazine_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['magazines'])
            & Q(codename__icontains='Article'))]

    create_group(GROUP_AUTHOR, (user_permissions+magazine_permissions))

def manager_group():
    user_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['users'])
            & Q(codename__icontains='User')
            | Q(codename__icontains='Subject'))]

    magazine_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['magazines'])
            & Q(codename__icontains='Publisher')
            | Q(codename__icontains='Number')
            | Q(codename__icontains='Magazine')
            | Q(codename__icontains='Article'))]


    create_group(GROUP_MANAGER, (user_permissions+magazine_permissions))

def editor_group():
    user_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['users'])
            & Q(codename__icontains='User'))]

    magazine_permissions = [
        p for p in Permission.objects.filter(
            Q(content_type__app_label__in=['magazines'])
            & Q(codename__icontains='Article'))]


    create_group(GROUP_EDITOR, (user_permissions+magazine_permissions))
