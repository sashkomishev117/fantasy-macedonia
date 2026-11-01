# FFM data pipeline

Scripts that collect Macedonian First League data from Transfermarkt and turn it
into the player dataset and price list used by the backend.

The `transfermarkt-api` package (v5.0.0) needs **Python 3.12 or 3.13**. It will
not install on Python 3.14.

## Setup

```bash
cd scraping
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Files

| File | Purpose |
|---|---|
| `my_scrape.py` | Fetches the 10 clubs of the league and each squad, writes `mk_first_league.csv` |
| `check.py` | Counts empty values per column and lists players with no position |
| `normalize_positions.py` | Groups detailed positions into GK / DEF / MID / FWD names |
| `fetch_stats.py` | Downloads each player's season-by-season stats into `stats_raw.json` (resumable) |
| `test_stats.py` | Small script used to inspect what `player_stats` returns |
| `history_check.py` | Shows how much league history each player has |
| `compute_prices.py` | Computes player prices, writes `prices.csv` |

Outputs: `mk_first_league.csv` and `prices.csv` are committed. `stats_raw.json`
is large and ignored by git; rebuild it with `python fetch_stats.py` (about 15
to 20 minutes, with a 3-second delay between requests).

## Datasets

### `mk_first_league.csv`

One row per player: 253 players across the 10 clubs of the 2026/27 season,
scraped on 1 November 2026.

| Column | Notes |
|---|---|
| team | Club name |
| id | Transfermarkt player id (primary key) |
| name, shirt_number, age, date_of_birth | |
| position | Goalkeeper / Defender / Midfielder / Forward |
| position_detail | The original Transfermarkt position (Centre-Back, Left Winger, ...) |
| nationality | Stored as list text, e.g. `['North Macedonia', 'Albania']`; the backend import converts it to `North Macedonia/Albania` |
| height, foot, signed_from, contract, market_value | Missing for some players, mostly youth |

### `prices.csv`

`id, name, team, position, est_per90, price`: the expected points per 90 minutes
and the resulting price in MKD (20,000 to 100,000, in steps of 5,000).

## Collecting the data

- The package is async: `Transfermarkt()` is used with `async with` and the
  script starts with `asyncio.run(main())`.
- The Macedonian First League has the competition id **`MAZ1`** (`MK1` returns
  "not found"). It was found with `search_competitions("Makedonska")`.
- `competition_clubs("MAZ1")` returns the clubs and `club_players(club.id)` the
  squads. `player_stats(player.id)` returns one row per player, competition and
  season.
- Requests wait 3 seconds between players to avoid being blocked.

## Data fixes

- 14 young players had no position on Transfermarkt's squad list. Their
  positions were looked up on Transfermarkt by hand and edited into the CSV, so
  **re-scraping overwrites those fixes**. An overrides file applied after
  scraping is a planned improvement.
- Detailed positions are grouped into four positions by `normalize_positions.py`;
  the original value is kept in `position_detail`.

## How prices are computed

`compute_prices.py` turns past results into a price. The constants at the top
of the file control it.

1. Only Macedonian First League rows (`MAZ1`) from the last five seasons are
   used. Recent seasons are weighted higher.
2. Each season row is converted to fantasy points with the game's scoring rules.
   Minutes count as `minutes / 45`.
3. Transfermarkt's `clean_sheets` and `goals_conceded` appear to count the
   *team's* results while the player was in the squad, so they are capped by the
   player's playing time. Without the cap, young players on strong defensive
   teams were priced like stars.
4. Points per 90 minutes are pulled toward the average of the player's position
   (shrinkage). The fewer minutes a player has, the stronger the pull. Players
   with no league minutes get a below-average estimate.
5. The estimate is converted linearly into a price between the floor and the
   cap. The best estimate in the league costs the cap.

The data has no saves, so goalkeepers are priced on minutes, clean sheets and
goals conceded.

Cheapest legal squad (respecting the 3-per-club limit) costs about 320,000 MKD
and the priciest about 1.1M, which is why the budget is 700,000 MKD.

## Notes

- This is a snapshot. Squads change with transfers, so re-scrape when you need
  fresh data. Re-scraping `mk_first_league.csv` overwrites the manual position
  fixes.
- Transfermarkt's terms restrict automated scraping. Keep the delay and avoid
  running the scripts repeatedly.

## Next steps

- [ ] Move the manual position fixes into an overrides file applied automatically
- [ ] Per-match stats for the current season, to feed the game's rounds