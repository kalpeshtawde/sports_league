from graphene_django import DjangoObjectType
import graphene

from tennis.models import League, Match, LeagueApplication, MatchRequest
from account.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filter_fields = [
            'email'
        ]


class LeagueType(DjangoObjectType):
    class Meta:
        model = League
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filter_fields = [
            'name',
            'city',
            'state',
            'country',
            'level',
        ]


class MatchType(DjangoObjectType):
    class Meta:
        model = Match
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filter_fields = [
            'player_one',
            'player_two',
            'player_three',
            'player_four',
            'league',
            'winner_one',
            'winner_two',
        ]


class LeagueApplicationType(DjangoObjectType):
    class Meta:
        model = LeagueApplication
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filter_fields = [
            'league',
            'players',
            'status',
        ]


class MatchRequestType(DjangoObjectType):
    class Meta:
        model = MatchRequest
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filter_fields = [
            'requested_by',
            'accepted_by',
            'format',
            'court',
            'match_time',
            'league',
            'created_at',
            'expiry_at',
        ]
