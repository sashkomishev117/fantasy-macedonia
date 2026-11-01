import json
from collections import Counter

from django.core.management.base import BaseCommand

from game.models import Player

NEED = {"GK": 2, "DEF": 5, "MID": 5, "FWD": 3}
START = {"GK": 1, "DEF": 4, "MID": 4, "FWD": 2}


class Command(BaseCommand):
    help = "Write the cheapest legal squad to /tmp/squad.json for API testing"

    def handle(self, *args, **options):
        per_club = Counter()
        squad = {}
        for pos, n in NEED.items():
            squad[pos] = []
            for p in Player.objects.filter(position=pos, price__isnull=False).order_by("price", "id"):
                if len(squad[pos]) == n:
                    break
                if per_club[p.team_id] < 3:
                    squad[pos].append(p)
                    per_club[p.team_id] += 1

        players = [p.id for pos in NEED for p in squad[pos]]
        starters = [p.id for pos in NEED for p in squad[pos][:START[pos]]]
        payload = {"name": "Test FC", "players": players,
                   "starters": starters, "captain": starters[0]}
        with open("/tmp/squad.json", "w") as f:
            json.dump(payload, f)
        self.stdout.write(self.style.SUCCESS(f"Wrote {len(players)} players to /tmp/squad.json"))