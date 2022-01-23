from django.core.management import BaseCommand

from tennis.factories import UserFactory, LeagueFactory, MatchFactory, MatchRequestFactory,\
    MessagingFactory
from tennis.models import League, Match, MatchRequest


class Command(BaseCommand):
    help = "Creates dummy data for tennis app"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating the new Things for our app")
        print(f"@@@@ Running for User Factory")
        for i in range(200):
            UserFactory()

        print(f"@@@@ Running for League Factory")
        LeagueFactory()

        print(f"@@@@ Running for Match Factory")
        for i in range(5000):
            MatchFactory()
        Match.objects.exclude(match_status__in=['completed']).update(winner_one=None, winner_two=None)
        for m in Match.objects.filter(match_status='completed'):
            player = m.player_one
            m.winner_one = player
            m.winner_two = None
            m.save()

        print(f"@@@@ Running for Match Request Factory")
        for i in range(50):
            MatchRequestFactory()

        print(f"@@@@ Running for Chat Factory")
        for i in range(1000):
            MessagingFactory()
