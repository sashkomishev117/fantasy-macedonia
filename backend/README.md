# FFM backend

Django 6 and Django REST Framework API for the game: players, accounts, squads,
rounds and scoring. SQLite is used for development.

## Setup

Requires Python 3.13.

```bash
cd backend
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py import_players     # teams and players from ../scraping/mk_first_league.csv
python manage.py import_prices      # prices from ../scraping/prices.csv
python manage.py createsuperuser
python manage.py runserver
```

The admin is at `/admin/`. Run the tests with `python manage.py test game`.

## Models (`game/models.py`)

| Model | Purpose |
|---|---|
| `Team` | A club (id is the Transfermarkt club id) |
| `Player` | A player (id is the Transfermarkt player id), with position, price in MKD and profile data |
| `FantasyTeam` | A user's team: budget (700,000 MKD) and captain |
| `SquadSlot` | One of the 15 players in a fantasy team, flagged as starter or bench |
| `Round` | A matchday with a deadline |
| `PlayerRoundStats` | One player's stats in one round; points are calculated automatically on save |

## API

| Endpoint | Auth | Description |
|---|---|---|
| `GET /api/teams/` | none | All clubs |
| `GET /api/players/` | none | All players. Filters: `?position=GK\|DEF\|MID\|FWD`, `?team=<club id>`, `?search=<name>`, `?ordering=price` or `-price` |
| `GET /api/players/<id>/` | none | One player |
| `POST /api/register/` | none | `{"username", "password"}` (8+ characters) returns `{"token"}` and creates an empty fantasy team |
| `POST /api/login/` | none | `{"username", "password"}` returns `{"token"}` |
| `GET /api/squad/` | token | Your squad, budget, amount spent and remaining |
| `PUT /api/squad/` | token | Save the squad: `{"name", "players": [15 ids], "starters": [11 ids], "captain": id}`. Returns `{"errors": [...]}` with status 400 if the rules are broken |

Send the token as `Authorization: Token <token>`.

## Rules and scoring code

| File | Purpose |
|---|---|
| `game/squad.py` | `validate_squad`: composition (2/5/5/3), max 3 per club, budget, legal starting 11, captain is a starter |
| `game/scoring.py` | `calculate_points`: points for one player in one match |
| `game/round_scoring.py` | Team points for a round: starters' points, captain doubled |

All three are covered by tests (`game/tests.py`, `game/test_scoring.py`,
`game/test_round_scoring.py`).

## Management commands

| Command | Purpose |
|---|---|
| `import_players` | Load teams and players from the scraped CSV (safe to re-run) |
| `import_prices` | Load prices and print the cheapest and priciest legal squad |
| `make_test_squad` | Write a legal test squad to `/tmp/squad.json` for API testing |
| `show_round_points <n>` | Print the fantasy team ranking for round n |
| `debug_round <n>` | Show which stats rows count for each team in round n |

## Entering stats by hand

In the admin, create a **Round** and then **Player round stats** rows. Fill in
**goals conceded** (the goals the player's team conceded in the match) on every
row. It defaults to 0, so a forgotten value gives every player who played 60
minutes a clean sheet.

## Not built yet

- Squads frozen at the round deadline (currently points use the current squad)
- Transfers, with a free transfer per round and a penalty for extras
- Bench substitutions when a starter does not play
- Leaderboard endpoint
- Loading real match data