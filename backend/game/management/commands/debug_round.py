from django.core.management.base import BaseCommand

from game.models import FantasyTeam, PlayerRoundStats, Round


class Command(BaseCommand):
    help = "Show which stats rows count for each team in a round"

    def add_arguments(self, parser):
        parser.add_argument("round", type=int)

    def handle(self, *args, **options):
        round_ = Round.objects.get(number=options["round"])
        stats = {s.player_id: s for s in PlayerRoundStats.objects.filter(round=round_)}
        self.stdout.write(f"{len(stats)} stats rows in {round_}")

        for team in FantasyTeam.objects.all():
            self.stdout.write(f"\n{team.name} (captain id: {team.captain_id})")
            for slot in team.slots.select_related("player"):
                row = stats.get(slot.player_id)
                role = "STARTER" if slot.is_starter else "bench"
                pts = row.points if row else "no stats row"
                self.stdout.write(f"  {role:8} {slot.player.name}: {pts}")