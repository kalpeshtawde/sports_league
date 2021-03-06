from graphene_django import DjangoObjectType
import graphene

from tennis.models import League, Match, LeagueApplication, MatchRequest, \
    MatchSet, UserEnquiry
from messaging.models import Messaging
from account.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"
        interfaces = (graphene.relay.Node,)


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
            'start_date',
            'end_date',
            'status',
            'winner_one',
            'winner_two',
        ]


class MatchType(DjangoObjectType):
    class Meta:
        model = Match
        fields = "__all__"
        interfaces = (graphene.relay.Node,)


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
            'league_app_id',
            'league__league_id',
            'league__city',
            'league__state',
            'league__status',
            'applicant__user_id',
            'applicant',
            'status',
        ]


class MatchRequestType(DjangoObjectType):
    class Meta:
        model = MatchRequest
        fields = "__all__"
        interfaces = (graphene.relay.Node,)
        filter_fields = [
            'match_request_id',
            'requested_by__user_id',
            'requested_to__user_id',
            'accepted_by__user_id',
            'format',
            'location',
            'court',
            'match_date',
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


class UserQueryType(DjangoObjectType):
    class Meta:
        model = UserEnquiry
        fields = "__all__"
        filter_fields = "__all__"
        interfaces = (graphene.relay.Node,)


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
    picture = graphene.String()
    rating = graphene.String()


class LeagueUserStatType(graphene.ObjectType):
    user_name = graphene.String()
    picture = graphene.String()
    rating = graphene.String()
    user_id = graphene.String()
    total = graphene.Int()
    won = graphene.Int()
    loss = graphene.Int()


class LeagueStatType(graphene.ObjectType):
    league_id = graphene.String()
    name = graphene.String()
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    level = graphene.String()
    description = graphene.String()
    status = graphene.String()
    format = graphene.String()
    winner_one_id = graphene.String()
    winner_two_id = graphene.String()
    user_stat = graphene.List(LeagueUserStatType)


class MatchRequestInput(graphene.InputObjectType):
    requested_by = graphene.String()
    requested_to = graphene.String()
    accepted_by = graphene.String()
    match_request_id = graphene.String()
    format = graphene.String()
    location = graphene.String()
    court = graphene.String()
    match_date = graphene.Date()
    match_time = graphene.Time()
    league_id = graphene.Float()


class LeagueInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    start_date = graphene.DateTime()
    end_date = graphene.DateTime()
    level = graphene.Float()
    description = graphene.String()


class MatchSetInput(graphene.InputObjectType):
    match_id = graphene.String()
    match_set_id = graphene.String()
    player_one_score = graphene.Int()
    player_two_score = graphene.Int()
    player_one_tb_score = graphene.Int()
    player_two_tb_score = graphene.Int()


class MatchInput(graphene.InputObjectType):
    match_id = graphene.String()
    player_one_id = graphene.String()
    player_two_id = graphene.String()
    player_three_id = graphene.String()
    player_four_id = graphene.String()
    league = graphene.String()
    format = graphene.String()
    winner_one = graphene.String()
    winner_two = graphene.String()
    match_status = graphene.String()
    court = graphene.String()
    start_date = graphene.Date()
    end_date = graphene.Date()
    set_1 = MatchSetInput()
    set_2 = MatchSetInput()
    set_3 = MatchSetInput()
    set_4 = MatchSetInput()
    set_5 = MatchSetInput()


class MessagingInput(graphene.InputObjectType):
    sender = graphene.String()
    recipient = graphene.String()
    message = graphene.String()


class UserQueryInput(graphene.InputObjectType):
    userid = graphene.String()
    message = graphene.String()
