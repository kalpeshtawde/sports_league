from django.core.management import BaseCommand

from tennis.factories import UserFactory, LeagueFactory, MatchFactory, MatchRequestFactory,\
    MessagingFactory


class Command(BaseCommand):
    help = "Creates dummy data for tennis app"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating the new Things for our app")
        print(f"@@@@ Running for User Factory")
        for i in range(20):
            UserFactory()

        print(f"@@@@ Running for League Factory")
        LeagueFactory()

        print(f"@@@@ Running for Match Factory")
        for i in range(50):
            MatchFactory()

        print(f"@@@@ Running for Match Request Factory")
        for i in range(50):
            MatchRequestFactory()

        print(f"@@@@ Running for Chat Factory")
        for i in range(1000):
            MessagingFactory()
