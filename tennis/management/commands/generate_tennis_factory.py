from django.core.management import BaseCommand
from django.db import transaction
from tennis.factories import UserFactory, LeagueFactory, MatchFactory, MatchRequestFactory


class Command(BaseCommand):
    help = "Creates dummy data for tennis app"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Creating the new Things for our app")
        for i in range(20):
            UserFactory()

        LeagueFactory()

        for i in range(50):
            MatchFactory()

        for i in range(50):
            MatchRequestFactory()
