from graphene_django import DjangoObjectType

from tennis.models import League, Match
from account.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            'email',
            'gender',
            'height',
            'level',
            'phone',
            'picture',
            'city',
            'state',
            'country',
        )


class LeagueType(DjangoObjectType):
    class Meta:
        model = League
        fields = ('id', 'name')


class MatchType(DjangoObjectType):
    class Meta:
        model = Match
        fields = ('id', 'player_one', 'player_two')


