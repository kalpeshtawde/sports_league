import graphene
from graphene_django.filter import DjangoFilterConnectionField

from gql.types import UserType, LeagueType, MatchType,\
    LeagueApplicationType, MatchRequestType, MessagingType
from tennis.models import League, Match

# Query
class Query(graphene.ObjectType):
    all_users = DjangoFilterConnectionField(UserType)
    all_leagues = DjangoFilterConnectionField(LeagueType)
    all_matches = DjangoFilterConnectionField(MatchType)
    all_match_requests = DjangoFilterConnectionField(MatchRequestType)
    all_league_applications = DjangoFilterConnectionField(LeagueApplicationType)
    all_messagings = DjangoFilterConnectionField(MessagingType)


# Mutation
class LeagueInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    city = graphene.String()
    state = graphene.String()
    country = graphene.String()
    start_date = graphene.DateTime()
    end_date = graphene.DateTime()
    level = graphene.Float()
    description = graphene.String()


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


class Mutation(graphene.ObjectType):
    create_league = CreateLeague.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
