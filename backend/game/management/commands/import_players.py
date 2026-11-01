import ast
import csv
from datetime import date

from django.conf import settings
from django.core.management.base import BaseCommand

from game.models import Player, Team

CSV_PATH = settings.BASE_DIR.parent / "scraping" / "mk_first_league.csv"

TEAM_IDS = {
    "Shkendija Tetovo": 1167,
    "Vardar Skopje": 77,
    "Sileks Kratovo": 535,
    "Struga Trim & Lum": 64534,
    "Tikves Kavadarci": 8969,
    "Arsimi": 101280,
    "Bregalnica Stip": 9892,
    "Shkendija Haracine 77": 123287,
    "Bashkimi": 8334,
    "FK Skopje": 21774,
}

POSITION_CODES = {
    "Goalkeeper": "GK",
    "Defender": "DEF",
    "Midfielder": "MID",
    "Forward": "FWD",
}


def to_int(value):
    """CSV cell -> int, or None if the cell is empty."""
    return int(value) if value else None


def to_date(value):
    return date.fromisoformat(value) if value else None


def clean_nationality(value):
    """"['North Macedonia', 'Albania']" -> "North Macedonia/Albania" """
    return "/".join(ast.literal_eval(value)) if value else ""


class Command(BaseCommand):
    help = "Import teams and players from scraping/mk_first_league.csv"

    def handle(self, *args, **options):
        with open(CSV_PATH, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        for name, team_id in TEAM_IDS.items():
            Team.objects.update_or_create(id=team_id, defaults={"name": name})

        for row in rows:
            Player.objects.update_or_create(
                id=int(row["id"]),
                defaults={
                    "team_id": TEAM_IDS[row["team"]],
                    "name": row["name"],
                    "position": POSITION_CODES[row["position"]],
                    "position_detail": row["position_detail"],
                    "shirt_number": to_int(row["shirt_number"]),
                    "date_of_birth": to_date(row["date_of_birth"]),
                    "nationality": clean_nationality(row["nationality"]),
                    "height": to_int(row["height"]),
                    "foot": row["foot"],
                    "market_value": to_int(row["market_value"]),
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f"Imported {Team.objects.count()} teams and {Player.objects.count()} players"
        ))