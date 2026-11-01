# FFM: Fantasy Football Macedonia

A fantasy football game built on the real teams and players of the Macedonian
First League (Prva Makedonska Fudbalska Liga). The goal is to give fans a reason
to follow every match and to keep improving the game over time.

## Status

Early development. The data pipeline and the game backend work end to end;
there is no frontend yet.

- [x] Player and team data scraped from Transfermarkt (253 players, 10 clubs, 2026/27)
- [x] Player prices (MKD) computed from past league performance
- [x] Django backend: players, teams, accounts, squads, rounds and scoring
- [x] Squad rules validated and tested
- [ ] Freeze squads at the round deadline
- [ ] Transfers (free transfer per round, penalty for extras)
- [ ] Bench substitutions
- [ ] Leaderboard endpoint
- [ ] Real match data (instead of typing stats into the admin)
- [ ] Web frontend (responsive, phone-first)
- [ ] Deployment
- [ ] Native iOS and Android apps

## Game rules (v1)

**Squad:** 15 players: 2 goalkeepers, 5 defenders, 5 midfielders, 3 forwards.
At most 3 players from the same club.

**Budget:** 700,000 MKD. Each player has a price between 20,000 and 100,000 MKD.

**Lineup:** 11 starters and 4 on the bench. Exactly 1 goalkeeper, at least
3 defenders, 2 midfielders and 1 forward start. The captain must be a starter
and scores double.

**Points per match:**

| Event | Points |
|---|---|
| Played 1 to 59 minutes | 1 |
| Played 60+ minutes | 2 |
| Goal (GK / DEF) | 6 |
| Goal (MID) | 5 |
| Goal (FWD) | 4 |
| Assist | 3 |
| Clean sheet, 60+ minutes (GK / DEF) | 4 |
| Clean sheet, 60+ minutes (MID) | 1 |
| Every 2 goals conceded (GK / DEF) | -1 |
| Yellow card | -1 |
| Red card | -3 |

Saves are not scored because the data source does not provide them.

## How prices work

Prices are based on how many fantasy points a player is expected to score, not
on Transfermarkt's market value. The pipeline uses Macedonian First League
results from the last five seasons (recent seasons count more), converts them
to points per 90 minutes with the rules above, and pulls players with few
minutes toward the average for their position. Players with no league history
get a below-average estimate. Details are in
[`scraping/README.md`](scraping/README.md).

## Project structure

```
fantasy-macedonia/
├── scraping/    Data collection, price model and the datasets (Python)
├── backend/     Django + Django REST Framework API (Python)
└── README.md
```

- [`scraping/README.md`](scraping/README.md): how the data is collected and how prices are computed
- [`backend/README.md`](backend/README.md): setup, API endpoints, models and tests

## Tech stack

- **Backend:** Django 6 and Django REST Framework, token authentication, SQLite for development
- **Data:** the `transfermarkt-api` Python package (needs Python 3.12 or 3.13)
- **Planned frontend:** a responsive React web app (installable as a PWA), then a native app with Expo that uses the same API

## Getting started

The two Python parts have separate virtual environments. Set up the backend
first, since it only needs the CSV files that are already in the repo:

```bash
cd backend
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py import_players
python manage.py import_prices
python manage.py createsuperuser
python manage.py runserver
```

See [`backend/README.md`](backend/README.md) for the API and
[`scraping/README.md`](scraping/README.md) to refresh the data.

## Roadmap

1. Freeze every squad at the round deadline so later changes cannot affect past points
2. Leaderboard endpoint and transfers
3. Bench substitutions
4. Automatic match data loading
5. React frontend, then deployment (Docker, PostgreSQL, HTTPS, CI)
6. Native apps

## Data source and legal note

Player data comes from Transfermarkt through an unofficial package, for personal
and development use. Transfermarkt's terms restrict automated scraping, so
requests are rate-limited and results are saved locally instead of being
fetched repeatedly. Check the terms and the licensing of the data before
launching the game publicly.

## Author

Sashko