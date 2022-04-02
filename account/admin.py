from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _


User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define admin model for custom User model with no email field."""

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = (
        'email', 'first_name', 'last_name', 'is_staff', 'gender',
        'height', 'rating', 'phone', 'city', 'state', 'country'
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


