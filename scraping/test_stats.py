import asyncio
from transfermarkt_api import Transfermarkt


async def main():
    async with Transfermarkt() as tm:
        stats = await tm.player_stats("66472")   # Besart Ibraimi, a long career
        print("Fields:", list(type(stats).model_fields))
        print(stats)


asyncio.run(main())