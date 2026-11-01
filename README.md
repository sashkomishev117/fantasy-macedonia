# FFM: Fantasy Football Macedonia

A fantasy football web game built on the real teams and players of the
Macedonian First League (Prva Makedonska Fudbalska Liga).

## Why

The goal is to get more people watching Macedonian football and to keep
improving the game over time. Fantasy games give fans a reason to follow every
match, including the ones they would otherwise skip.

## Status

Early development. So far:

- [x] Player and team data scraped from Transfermarkt (253 players, 10 clubs, 2026/27 season)
- [ ] Game design and rules
- [ ] Backend and database
- [ ] Web frontend
- [ ] Match results and points scoring
- [ ] Deployment

## How it works

<!-- TODO: describe the game in a few lines. For example: how many players
a user picks, the budget or constraints, how points are scored. -->

## Project structure

```
fantasy-macedonia/
├── scraping/          Data collection scripts and the scraped dataset
│   ├── my_scrape.py
│   ├── check.py
│   ├── normalize_positions.py
│   ├── mk_first_league.csv
│   └── README.md      Details about the scraper and the data
└── README.md
```

<!-- TODO: add the app folders (frontend, backend, ...) as they are created. -->

## Data

Team and player data comes from Transfermarkt through the `transfermarkt-api`
Python package. The dataset (`scraping/mk_first_league.csv`) has one row per
player with team, position, age, nationality and market value. Positions are
grouped into Goalkeeper, Defender, Midfielder and Forward for the game.

See [`scraping/README.md`](scraping/README.md) for how the data is collected,
known gaps (some youth players have missing fields) and how to refresh it.

## Getting started

Scraping environment (requires Python 3.12 or 3.13, not 3.14):

```bash
cd scraping
python3.13 -m venv .venv
source .venv/bin/activate
pip install transfermarkt-api
python my_scrape.py
```

<!-- TODO: add setup and run instructions for the web app. -->

## Tech stack

<!-- TODO: fill in. For example: frontend, backend, database, hosting. -->

## Roadmap

- Decide on the scoring system and squad rules
- Load the player data into a database, using the Transfermarkt player id as the key
- Build the team selection and leaderboard pages
- Add a way to update match results and player points after each round
- Refresh squad data regularly as transfers happen

## Data source and legal note

Player data is scraped from Transfermarkt for personal and development use.
Transfermarkt's terms restrict automated scraping, so requests are rate-limited
and data is saved locally instead of being fetched repeatedly. Check the terms
and consider the licensing of the data before launching the game publicly.

## Author

Sashko
