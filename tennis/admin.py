from django.contrib import admin

from .models import League, LeagueApplication, Match


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


@admin.register(LeagueApplication)
class LeagueApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'league',
        'applicant',
        'status',
    )
    search_fields = (
        'league',
    )

    #def players(self, obj):
    #    return "\n".join([a.player_name for a in obj.players_set.all()])


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
