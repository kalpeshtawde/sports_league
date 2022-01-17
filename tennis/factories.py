import factory
import random
from factory import fuzzy
from datetime import datetime
from dateutil.relativedelta import relativedelta

from account.models import User
from tennis.models import League, Match


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.LazyAttribute(
        lambda a: "{0}.{1}@test.com".format(a.first_name, a.last_name).lower()
    )
    gender = fuzzy.FuzzyChoice(User.GENDER_CHOICES, getter=lambda c: c[0])
    height = fuzzy.FuzzyInteger(3, 8)
    level = fuzzy.FuzzyInteger(1, 10)
    phone = factory.Sequence(lambda n: '123-555-%04d' % n)
    city = "Portland"
    state = "Oregon"
    country = "USA"


class LeagueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = League

    name = "Portland tennis leagues 4.5"
    city = "Portland"
    state = "Oregon"
    country = "USA"
    start_date = datetime.today() + relativedelta(months=1)
    end_date = datetime.today() + relativedelta(months=3)
    level = "3.5"
    description = name


class MatchFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Match

    player_one = factory.SubFactory(UserFactory)
    player_two = factory.SubFactory(UserFactory)
    league = factory.Iterator(League.objects.all())
    type = fuzzy.FuzzyChoice(Match.MATCH_CHOICES, getter=lambda c: c[0])
    winner_one = random.choice([player_one, player_two])
    start_date = fuzzy.FuzzyNaiveDateTime(
        datetime.today() + relativedelta(months=1),
        datetime.today() + relativedelta(months=3)
    )
    end_date = start_date
