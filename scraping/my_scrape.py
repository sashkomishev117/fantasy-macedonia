import asyncio 
import csv
from transfermarkt_api import Transfermarkt

COLUMNS = ["team", "id", "name", "position", "shirt_number", "age",
           "date_of_birth", "nationality", "height", "foot",
           "signed_from", "contract", "market_value"]

async def main():
    rows = []
    async with Transfermarkt() as tm:
        result = await tm.competition_clubs("MAZ1")

        for club in result.clubs:
            print("Fetching:", club.name)
            squad = await tm.club_players(club.id)

            for player in squad.players:
                row = player.model_dump(mode="json")
                row["team"] = club.name
                row["nationality"] = player.nationality
                rows.append(row)

            await asyncio.sleep(3)

    with open("mk_first_league.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print("Saved", len(rows), "players")

asyncio.run(main())