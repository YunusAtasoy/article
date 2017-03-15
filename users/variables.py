from django.utils.translation import ugettext_lazy as _


USER_AUTHOR, USER_MANAGER, USER_EDITOR = (0, 1, 2)
USER_TYPES = (
    (USER_AUTHOR, _('AUTHOR')),
    (USER_MANAGER, _('MANAGER')),
    (USER_EDITOR, _('EDITOR'))
)


#Group

GROUP_AUTHOR = 'Author'
GROUP_MANAGER = 'Manager'
GROUP_EDITOR = 'Editor'



CONFIRM, EDIT, WAITING = (0, 1, 2)
CONFIRM_TYPES = (
    (CONFIRM, _('CONFIRM')),
    (EDIT, _('EDIT')),
    (WAITING, _('WAITING'))
    )
