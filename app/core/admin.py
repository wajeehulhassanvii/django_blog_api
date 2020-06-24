from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# we use translation in case we want to support multiple languages later on
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):

    # we want to order according to ID
    ordering = ['id']
    # we want to list them by email and first_name
    list_display = ['email', 'first_name']
    # The fields to be displayed
    fieldsets = (
        # first we define sections
        # first section
        (None, {'fields': ('email', 'password')}),
        # second section
        (_('Personal Info'), {'fields': ('first_name', 'last_name')}),
        # third section
        (
            _('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser',\
                           'is_author')
            }
        ),
        # fourth section
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    # add_fields for adding values for user in add page
    add_fieldsets = (
        (None, {
            # classes assigned to form
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),  # extra comma in the end so python know its a list
    )


# register models in admin
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Post)