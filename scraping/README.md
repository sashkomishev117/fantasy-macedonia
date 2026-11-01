# FFM data scraping

Scripts that collect Macedonian First League data (teams and players) from
Transfermarkt for the FFM fantasy football game.

## Data

`mk_first_league.csv` has one row per player: 253 players across the 10 clubs
of the 2026/27 Prva Makedonska Fudbalska Liga, scraped on 1 Nov 2026.

| Column | Notes |
|---|---|
| team | Club name |
| id | Transfermarkt player id (use as the primary key) |
| name, shirt_number, age, date_of_birth | |
| position | Goalkeeper / Defender / Midfielder / Forward (see below) |
| nationality | Stored as a Python-style list, e.g. `['North Macedonia']` |
| height, foot, signed_from, contract, market_value | Missing for some players |

Missing values are empty cells. Height and foot are often blank for youth
players. Market value is in euros.

## Setup

The `transfermarkt-api` package (v5.0.0) needs Python 3.12 or 3.13. It will not
install on Python 3.14, which is the Fedora default.

```bash
cd scraping
python3.13 -m venv .venv
source .venv/bin/activate
pip install transfermarkt-api
```

## Scripts

| File | Purpose |
|---|---|
| `my_scrape.py` | Fetches all clubs of the league, then each club's squad, and writes `mk_first_league.csv` |
| `check.py` | Counts empty values per column and lists players with no position |
| `normalize_positions.py` | Groups detailed positions into four fantasy positions |

Run the scraper with `python my_scrape.py`.

## How the scraper works

- The package is async: `Transfermarkt()` is used with `async with`, and the
  script is started with `asyncio.run(main())`.
- The Macedonian First League has the competition id **`MAZ1`**. The id `MK1`
  returns "not found". It was found with `search_competitions("Makedonska")`.
- `competition_clubs("MAZ1")` returns the 10 clubs, and `club_players(club.id)`
  returns each squad.
- Each player is converted with `model_dump(mode="json")`, the club name is
  added as `team`, and the nationality list is joined into one string.
- There is a 3-second delay between requests to avoid being blocked.

## Data fixes

- 14 players (mostly recently registered youth players) had no position on
  Transfermarkt's squad list. Their positions were looked up on Transfermarkt
  by hand and filled in.
- Detailed positions (Centre-Back, Left Winger, Attacking Midfield, ...) are
  grouped into Goalkeeper, Defender, Midfielder and Forward by
  `normalize_positions.py`. The original value is kept in `position_detail`.

## Notes

- This is a snapshot. Squads change with transfers, so re-scrape when you need
  fresh data. Re-scraping overwrites the CSV, including the manual fixes.
- Transfermarkt's terms restrict automated scraping, so keep the delay and avoid
  running the script repeatedly.
- `.venv/` is in `.gitignore`.

## Next steps

- [ ] Run `normalize_positions.py` and commit the result
- [ ] Move the manual position fixes into an overrides file applied automatically after scraping
- [ ] Export a JSON grouped by team for the web app
- [ ] Load the data into a database (SQLite), with the player id as key
