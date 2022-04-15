from django_filters import FilterSet, OrderingFilter, CharFilter
from django.db.models import Q

from tennis.models import Match
from account.models import User
from messaging.models import Messaging


class MatchFilter(FilterSet):
    user_search = CharFilter(
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

    order_by = OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
        )
    )

    def user_filter(self, queryset, name, value):
        return Match.objects.filter(
            Q(player_one__user_id=value) |
            Q(player_two__user_id=value) |
            Q(player_three__user_id=value) |
            Q(player_four__user_id=value)
        )


class UserFilter(FilterSet):
    user_name_search = CharFilter(
        method='user_name_filter', label='User Name Search'
    )

    class Meta:
        model = User
        fields = [
            'user_name_search',
            'user_id',
            'first_name',
            'last_name',
            'email',
            'gender',
            'height',
            'rating',
            'phone',
            'city',
            'state',
            'country',
            'active',
            'deleted',
        ]

    def user_name_filter(self, queryset, name, value):
        return User.objects.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value)
        )


class MessagingFilter(FilterSet):
    sender_receipient_search = CharFilter(
        method='sender_receipient_filter', label='Sender Receipient Search'
    )

    class Meta:
        model = Messaging
        fields = [
            'sender_receipient_search',
            'message_id',
            'message',
            'sender__user_id',
            'recipient__user_id',
            'created_at',
        ]

    order_by = OrderingFilter(
        fields=(
            ('created_at', 'created_at'),
        )
    )

    def sender_receipient_filter(self, queryset, name, value):
        if '|' in value:
            user_id = value.split('|')
            return Messaging.objects.filter(
                (Q(sender__user_id=user_id[0]) | Q(recipient__user_id=user_id[0])) &
                (Q(sender__user_id=user_id[1]) | Q(recipient__user_id=user_id[1]))
            )
        else:
            return Messaging.objects.filter(
                Q(sender__user_id=value) |
                Q(recipient__user_id=value)
            )
