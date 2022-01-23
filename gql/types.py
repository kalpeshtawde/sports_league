from graphene_django import DjangoObjectType
import graphene

from tennis.models import League, Match, LeagueApplication, MatchRequest
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


class MessagingType(DjangoObjectType):
    class Meta:
        model = Messaging
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filter_fields = [
            "message",
            "sender",
            "recipient",
            "created_at",
        ]


class UserProfileType(graphene.ObjectType):
    user_id = graphene.Int()
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
