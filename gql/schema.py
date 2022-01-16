import graphene

from gql.types import UserType, LeagueType, MatchType
from tennis.models import League, Match
from account.models import User

# Query


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    leagues = graphene.List(LeagueType)
    matches = graphene.List(MatchType)

    def resolve_matches(root, info, **kwargs):
        return User.objects.all()

    def resolve_leagues(root, info, **kwargs):
        return League.objects.all()

    def resolve_matches(root, info, **kwargs):
        return Match.objects.all()


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
