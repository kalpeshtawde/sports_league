import string
import random
import factory
import pytz
from factory import fuzzy
from datetime import datetime
from dateutil.relativedelta import relativedelta

from account.models import User
from messaging.models import Messaging
from tennis.models import League, Match, MatchRequest, MatchSet, \
    LeagueApplication


users = User.objects.all()


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
    phone = factory.Sequence(lambda n: '123-555-%04d' % n)
    city = "Portland"
    state = "Oregon"
    country = "USA"
    rating = fuzzy.FuzzyChoice(['3.0', '3.5', '4.0', '4.5', '5.0', '5.5', '6.0'])
    dob = factory.Faker("date_of_birth", minimum_age=8)
    about_me = "I am 4.0, available to play weekdays evening and on weekends."
    active = fuzzy.FuzzyChoice([True, False])
    picture = "default.png"
    deleted = fuzzy.FuzzyChoice([True, False])


class LeagueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = League
    name = fuzzy.FuzzyInteger(1, 10000)
    city = "Portland"
    state = "Oregon"
    country = "USA"
    start_date = datetime.utcnow().replace(tzinfo=pytz.utc) + relativedelta(months=1)
    end_date = datetime.utcnow().replace(tzinfo=pytz.utc) + relativedelta(months=3)
    level = "3.5"
    description = name
    status = fuzzy.FuzzyChoice(["ongoing", "completed"])


# class MatchRequestFactory(factory.django.DjangoModelFactory):
#     class Meta:
#         model = MatchRequest
#
#     requested_by = random.choice(users)
#     accepted_by = random.choice(users)
#     format = fuzzy.FuzzyChoice(MatchRequest.MATCH_CHOICES, getter=lambda c: c[0])
#     court = 'Gabriel Park, Portland'
#     match_time = "16:00"
#     league = factory.Iterator(League.objects.all())
