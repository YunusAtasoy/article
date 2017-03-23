from django.contrib import admin
from .models import User, Subject
from copy import deepcopy
from django.shortcuts import get_object_or_404

# Django
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.utils.translation import ugettext_lazy as _

# Local Django
from .forms import UserChangeForm
from .variables import (
    GROUP_AUTHOR, GROUP_MANAGER, GROUP_EDITOR
)
from .variables import (
        USER_AUTHOR, USER_MANAGER,
        USER_EDITOR, USER_TYPES
)

###    User    ###

class UserAdmin(_UserAdmin):
    actions = ['delete_selected']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_types',
                       'password1', 'password2', 'is_developer')}
        ),
    )

    fieldsets = (
        (_(u'Base Informations'), {
            'fields' : ('email', 'password'),
        }),
        (_(u'Personal Informations'), {
            'fields' : ('first_name', 'last_name')
        }),
        (_(u'Important Informations'), {
            'fields' : ('user_types', 'last_login')
        }),
        (_(u'Permissions'), {
            'fields' : ('is_active', 'is_staff', 'is_developer','groups')
        }),
    )



    form = UserChangeForm

    list_display = ('first_name', 'last_name', 'email', 'user_types',
                    'is_active', 'is_staff', 'is_developer', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_developer', 'user_types')
    search_fields = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login',)
    ordering = ('first_name', 'last_name')


    def get_fieldsets(self, request, obj=None):
        fieldsets = super(UserAdmin, self).get_fieldsets(request, obj)

        custom_fieldsets = deepcopy(fieldsets)

        if not request.user.is_superuser:

            group_names = [group.name for group in request.user.groups.all()]
            if not GROUP_MANAGER in group_names:
                custom_fieldsets = [
                    field for field in custom_fieldsets if field[0] !=
                        _('Permissions')
                        ]

            for fieldset in custom_fieldsets:
                fields = [
                    field for field in fieldset[1]['fields'] if field !=
                        'is_superuser'
                        ]
                fieldset[1]['fields'] = fields

        return custom_fieldsets

    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            qs = qs.exclude(is_superuser=True)

            group_names = [group.name for group in request.user.groups.all()]
            if not GROUP_MANAGER in group_names:
                qs = qs.filter(pk=request.user.id)

        return qs

    def delete_model(self, request, queryset):
        if not queryset.is_superuser:
            queryset.delete()

    def delete_selected(self, request, obj):
        for user in obj.all():
            if not user.is_superuser:
                user.delete()

    delete_selected.short_description = _("Delete selected Users")

    def get_actions(self, request):
        actions = super(UserAdmin, self).get_actions(request)

        group_names = [group.name for group in request.user.groups.all()]
        if not request.user.is_superuser and  not GROUP_MANAGER in group_names:
            del actions['delete_selected']

        return actions

    def has_add_permission(self, request):
        group_names = [group.name for group in request.user.groups.all()]
        if request.user.is_superuser or GROUP_MANAGER in group_names:
            return True
        else:
            return False

    def has_delete_permission(self, request, obj=None):
        group_names = [group.name for group in request.user.groups.all()]
        if request.user.is_superuser or GROUP_MANAGER in group_names:
            return True
        else:
            return False




admin.site.register(User, UserAdmin)
admin.site.register(Subject)
