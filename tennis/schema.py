import graphene
from graphene_django import DjangoObjectType
from .models import League, Match


class LeagueType(DjangoObjectType):
    class Meta:
        model = League
        fields = ('id', 'name')


class MatchType(DjangoObjectType):
    class Meta:
        model = Match
        fields = ('id', 'player_one', 'player_two')


class Query(graphene.ObjectType):
    leagues = graphene.List(LeagueType)
    matches = graphene.List(MatchType)

    def resolve_leagues(root, info, **kwargs):
        return League.objects.all()

    def resolve_matches(root, info, **kwargs):
        return Match.objects.all()


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
