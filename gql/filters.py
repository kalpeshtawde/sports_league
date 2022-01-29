import django_filters
from django.db.models import Q

from tennis.models import Match


class MatchFilter(django_filters.FilterSet):
    user_search = django_filters.CharFilter(
        method='user_filter', label='User Search'
    )

    class Meta:
        model = Match
        fields = [
            'user_search',
            'match_id',
            'player_one__user_id',
            'player_two__user_id',
            'player_three__user_id',
            'player_four__user_id',
            'league',
            'winner_one',
            'winner_two',
        ]

    def user_filter(self, queryset, name, value):
        return Match.objects.filter(
            Q(player_one__user_id=value) |
            Q(player_two__user_id=value) |
            Q(player_three__user_id=value) |
            Q(player_four__user_id=value)
        )
