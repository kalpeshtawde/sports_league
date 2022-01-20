from django.core.management import BaseCommand
from django.db import transaction
from account.models import User
from messaging.models import Messaging
from tennis.models import League, Match, MatchRequest


class Command(BaseCommand):
    help="Deletes data form tennis app"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting Things from our app")

        User.objects.exclude(is_staff=True).delete()

        models = [League, Match, MatchRequest, Messaging]
        for m in models:
            print(f"@@@@ Running for model {m}")
            m.objects.all().delete()
