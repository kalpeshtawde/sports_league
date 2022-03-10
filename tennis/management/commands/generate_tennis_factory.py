import random
from uuid import uuid4
import pytz
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from django.db import transaction
from django.db.utils import IntegrityError
from django.core.management import BaseCommand

from tennis.factories import UserFactory, LeagueFactory, MatchRequestFactory,\
    MessagingFactory
from tennis.models import League, Match, MatchRequest, MatchSet
from account.models import User


class Command(BaseCommand):
    help = "Creates dummy data for tennis app"

    def random_date(self, start, end):
        """
        This function will return a random datetime between two datetime
        objects.
        """
        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start + timedelta(seconds=random_second)

    def run_user_factory(self):
        print(f"@@@@ Running for User Factory")
        for i in range(200):
            try:
                UserFactory()
            except IntegrityError:
                pass

    def run_league_factory(self):
        print(f"@@@@ Running for League Factory")
        for i in range(10):
            LeagueFactory()
        for league in League.objects.all():
            league.name = f"Portland tennis leagues 4.5 - {league.name}"
            league.save()
            if league.status == "completed":
                match = Match.objects.filter(league_id=league.league_id)
                if match:
                    user = match.first().player_one
                    if user:
                        league.winner_one = user
                        league.save()

    def run_match_factory(self):
        print(f"@@@@ Running for Match Factory")
        all_users = User.objects.all()
        print(f"all users count {all_users.count()}")
        for i in range(1000):
            player_one = all_users[random.choice(range(all_users.count()))]
            player_two = all_users[random.choice(range(all_users.count()))]
            league = random.choice(League.objects.all())
            match_format = random.choice(['single'])
            match_status = random.choice(['completed', 'draw', 'cancelled', 'pending'])
            start_date = self.random_date(
                datetime.utcnow().replace(tzinfo=pytz.utc) + relativedelta(months=-6),
                datetime.utcnow().replace(tzinfo=pytz.utc) + relativedelta(months=3),
                )
            end_date = start_date

            if player_one.user_id != player_two.user_id:
                m, flag = Match.objects.get_or_create(
                    player_one=player_one,
                    player_two=player_two,
                    league=league,
                    format=match_format,
                    winner_one=player_one,
                    match_status=match_status,
                    court='Gabriel Park, Portland',
                    start_date=start_date,
                    end_date=end_date,
                )
                # Create matches with 5 sets each
                for k in range(5):
                    ms, created = MatchSet.objects.get_or_create(
                        match_set_id=uuid4(),
                        match=m,
                        player_one_score=6,
                        player_two_score=3,
                    )

        Match.objects.exclude(match_status__in=['completed']).update(winner_one=None, winner_two=None)

        # Assign winner to the match
        for league in League.objects.all():
            if league.status == "completed":
                match = Match.objects.filter(league_id=league.league_id)
                if match:
                    user = match.first().player_one
                    if user:
                        league.winner_one = user
                        league.save()

    def run_match_request_factory(self):
        print(f"@@@@ Running for Match Request Factory")
        for i in range(50):
            MatchRequestFactory()

    def run_chat_factory(self):
        print(f"@@@@ Running for Chat Factory")
        for i in range(1000):
            MessagingFactory()

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating the new Things for our app")

        self.run_user_factory()
        self.run_league_factory()
        self.run_match_factory()
        self.run_match_request_factory()
        self.run_chat_factory()
