import string
import factory
from factory import fuzzy
from datetime import datetime
from dateutil.relativedelta import relativedelta

from account.models import User
from messaging.models import Messaging
from tennis.models import League, Match, MatchRequest, MatchSet


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
    dob = factory.Faker("date_of_birth", minimum_age=8)
    about_me = "I am 4.0, available to play weekdays evening and on weekends."
    active = fuzzy.FuzzyChoice([True, False])
    deleted = fuzzy.FuzzyChoice([True, False])


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


class MatchRequestFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MatchRequest

    requested_by = factory.Iterator(User.objects.all())
    accepted_by = factory.Iterator(User.objects.all())
    format = fuzzy.FuzzyChoice(MatchRequest.MATCH_CHOICES, getter=lambda c: c[0])
    court = 'Gabriel Park, Portland'
    match_time = "16:00"
    league = factory.Iterator(League.objects.all())


class MessagingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Messaging

    message = fuzzy.FuzzyText(length=20, chars=string.ascii_letters)
    sender = factory.Iterator(User.objects.all())
    recipient = factory.Iterator(User.objects.all())
