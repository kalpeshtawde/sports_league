from graphene_django import DjangoObjectType
import graphene

from tennis.models import League, Match, LeagueApplication, MatchRequest, MatchSet
from messaging.models import Messaging
from account.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filter_fields = [
            'first_name',
            'last_name',
            'email',
            'gender',
            'height',
            'level',
            'phone',
            'city',
            'state',
            'country',
            'active',
            'deleted',
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
            'player_one__user_id',
            'player_two__user_id',
            'player_three__user_id',
            'player_four__user_id',
            'league',
            'winner_one',
            'winner_two',
        ]


class MatchSetType(DjangoObjectType):
    class Meta:
        model = MatchSet
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filter_fields = [
            'match_set_id',
            'match',
            'player_one_score',
            'player_two_score',
            'player_one_tb_score',
            'player_two_tb_score',
        ]


class LeagueApplicationType(DjangoObjectType):
    class Meta:
        model = LeagueApplication
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filter_fields = [
            'league__league_id',
            'players',
            'status',
        ]


class MatchRequestType(DjangoObjectType):
    class Meta:
        model = MatchRequest
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filter_fields = [
            'requested_by__user_id',
            'accepted_by__user_id',
            'format',
            'court',
            'match_time',
            'league__league_id',
            'created_at',
            'expiry_at',
        ]


class MessagingType(DjangoObjectType):
    class Meta:
        model = Messaging
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filter_fields = [
            "message",
            "sender__user_id",
            "recipient__user_id",
            "created_at",
        ]


class UserProfileType(graphene.ObjectType):
    user_id = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    matches_count = graphene.Int()
    won_count = graphene.Int()
    draw_count = graphene.Int()
    lost_count = graphene.Int()
    city = graphene.String()
    state = graphene.String()
    dob = graphene.Date()
    age = graphene.Int()
