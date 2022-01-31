import graphene
from uuid import uuid4
from graphene_django.filter import DjangoFilterConnectionField

from gql.types import UserType, LeagueType, MatchType,LeagueApplicationType, \
    MatchRequestType, MessagingType, UserProfileType, MatchSetType, \
    LeagueInput, MatchRequestInput
from gql.resolvers import resolve_user_profiles
from gql.filters import MatchFilter
from tennis.models import League, Match, MatchRequest
from account.models import User


# Query
class Query(graphene.ObjectType):
    all_users = DjangoFilterConnectionField(UserType)
    all_leagues = DjangoFilterConnectionField(LeagueType)
    all_matches = DjangoFilterConnectionField(
        MatchType, filterset_class=MatchFilter)
    all_match_sets = DjangoFilterConnectionField(MatchSetType)
    all_match_requests = DjangoFilterConnectionField(MatchRequestType)
    all_league_applications = DjangoFilterConnectionField(LeagueApplicationType)
    all_messagings = DjangoFilterConnectionField(MessagingType)
    user_profiles = graphene.Field(
        UserProfileType,
        user_id=graphene.String(required=True),
    )

    def resolve_user_profiles(self, info, user_id):
        return resolve_user_profiles(user_id)


# Mutation
class CreateLeague(graphene.Mutation):
    class Arguments:
        input = LeagueInput(required=True)

    league = graphene.Field(LeagueType)

    @classmethod
    def mutate(cls, root, info, input):
        league = League()
        league.name = input.name
        league.city = input.city
        league.state = input.state
        league.country = input.country
        league.start_date = input.start_date
        league.end_date = input.end_date
        league.level = input.level
        league.description = input.description
        league.save()
        return CreateLeague(league=league)


class CreateMatchRequest(graphene.Mutation):
    class Arguments:
        input = MatchRequestInput(required=True)

    match_request = graphene.Field(MatchRequestType)

    @classmethod
    def mutate(cls, root, info, input):

        if not input.match_request_id:
            match_request = MatchRequest()
            match_request.match_request_id = uuid4()
        else:
            match_request = MatchRequest.objects.filter(
               match_request_id=input.match_request_id
            ).first()

        if input.requested_by:
            user = User.objects.filter(
                user_id=input.requested_by
            ).first()
            match_request.requested_by = user


        match_request.requested_to = input.requested_to
        match_request.accepted_by = input.accepted_by
        match_request.match_request_id = input.match_request_id
        match_request.format = input.format
        match_request.location = input.location
        match_request.court = input.court
        match_request.match_date = input.match_date
        match_request.match_time = input.match_time
        match_request.league = input.league_id
        match_request.save()

        return CreateMatchRequest(match_request=match_request)


class Mutation(graphene.ObjectType):
    league = CreateLeague.Field()
    match_request = CreateMatchRequest.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
