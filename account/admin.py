from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from tennis.models import League, Match


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
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'city',
        'state',
        'country',
        'start_date',
        'end_date',
        'level',
    )
    search_fields = (
        'name',
        'city',
        'state',
        'country',
        'players',
    )


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'player_one',
        'player_two',
        'player_three',
        'player_four',
        'league',
        'winner_one',
        'winner_two',
        'start_date',
        'end_date',
    )
    search_fields = (
        'league',
        'winner_one',
        'winner_two',
    )
