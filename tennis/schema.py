import graphene
from graphene_django import DjangoObjectType
from tennis.models import League, Match


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


schema = graphene.Schema(query=Query)