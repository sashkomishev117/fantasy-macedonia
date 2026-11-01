import asyncio
import csv
import json
import os

from transfermarkt_api import Transfermarkt
from transfermarkt_api.exceptions import NotFound

OUT = "stats_raw.json"


async def main():
    with open("mk_first_league.csv", encoding="utf-8") as f:
        players = list(csv.DictReader(f))

    # resume support: load what we already downloaded
    data = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            data = json.load(f)

    async with Transfermarkt() as tm:
        for p in players:
            if p["id"] in data:
                continue
            print("Fetching:", p["name"])
            try:
                result = await tm.player_stats(p["id"])
                data[p["id"]] = [s.model_dump(mode="json") for s in result.stats]
            except NotFound:
                print("  no stats found for", p["name"])
                data[p["id"]] = []

            with open(OUT, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)
            await asyncio.sleep(3)

    print("Saved stats for", len(data), "players")


asyncio.run(main())