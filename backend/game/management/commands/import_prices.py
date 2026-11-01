import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from game.models import Player

PRICES_PATH = settings.BASE_DIR.parent / "scraping" / "prices.csv"
SQUAD = {"GK": 2, "DEF": 5, "MID": 5, "FWD": 3}


class Command(BaseCommand):
    help = "Load player prices from scraping/prices.csv"

    def handle(self, *args, **options):
        with open(PRICES_PATH, encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        updated = 0
        for row in rows:
            updated += Player.objects.filter(id=int(row["id"])).update(
                price=int(row["price"])
            )
        self.stdout.write(self.style.SUCCESS(f"Updated prices for {updated} players"))

        # how loose or tight is a budget? cheapest and priciest legal 15-man squad
        cheapest = priciest = 0
        for pos, n in SQUAD.items():
            prices = sorted(
                Player.objects.filter(position=pos, price__isnull=False)
                .values_list("price", flat=True)
            )
            cheapest += sum(prices[:n])
            priciest += sum(prices[-n:])
        self.stdout.write(f"Cheapest squad: {cheapest:,} MKD | priciest: {priciest:,} MKD")