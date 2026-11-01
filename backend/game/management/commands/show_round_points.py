from django.core.management.base import BaseCommand

from game.models import FantasyTeam, Round
from game.round_scoring import compute_team_round_points


class Command(BaseCommand):
    help = "Print the fantasy team ranking for one round"

    def add_arguments(self, parser):
        parser.add_argument("round", type=int)

    def handle(self, *args, **options):
        round_ = Round.objects.get(number=options["round"])
        rows = sorted(
            ((compute_team_round_points(t, round_), t.name) for t in FantasyTeam.objects.all()),
            reverse=True,
        )
        for place, (points, name) in enumerate(rows, 1):
            self.stdout.write(f"{place}. {name}: {points}")