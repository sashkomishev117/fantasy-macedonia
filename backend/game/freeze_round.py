from django.core.management.base import BaseCommand

from game.freeze import freeze_round
from game.models import Round


class Command(BaseCommand):
    help = "Freeze all squads for a round (normally this happens automatically after the deadline)"

    def add_arguments(self, parser):
        parser.add_argument("round", type=int)

    def handle(self, *args, **options):
        try:
            round_ = Round.objects.get(number=options["round"])
        except Round.DoesNotExist:
            self.stderr.write(f"Round {options['round']} does not exist.")
            return
        if round_.is_frozen:
            self.stdout.write("Already frozen.")
            return
        saved = freeze_round(round_)
        self.stdout.write(self.style.SUCCESS(f"Froze {saved} squads for {round_}"))