import csv
import json
from collections import Counter

LEAGUE = "MAZ1"
SEASONS = {"2022", "2023", "2024", "2025", "2026"}   # last five; 2026 is the current, partial one

with open("mk_first_league.csv", encoding="utf-8") as f:
    players = {r["id"]: r for r in csv.DictReader(f)}

with open("stats_raw.json", encoding="utf-8") as f:
    stats = json.load(f)

rows = []
for pid, p in players.items():
    league = [s for s in stats.get(pid, [])
              if s["competition_id"] == LEAGUE and s["season_id"] in SEASONS]
    minutes = sum(s["minutes_played"] or 0 for s in league)
    seasons = sum(1 for s in league if (s["minutes_played"] or 0) > 0)
    rows.append((p["name"], p["team"], p["position"], minutes, seasons))


def bucket(m):
    if m == 0:
        return "0 min (no league history)"
    if m < 500:
        return "1-499 min"
    if m < 1500:
        return "500-1499 min"
    if m < 3000:
        return "1500-2999 min"
    return "3000+ min"


order = ["0 min (no league history)", "1-499 min", "500-1499 min", "1500-2999 min", "3000+ min"]
counts = Counter(bucket(r[3]) for r in rows)
print("Minutes in MAZ1, seasons 2022 to 2026:")
for b in order:
    print(f"  {b}: {counts[b]}")

print("\nSeasons with minutes played:", sorted(Counter(r[4] for r in rows).items()))

print("\nNo history, by position:", dict(Counter(r[2] for r in rows if r[3] == 0)))

print("\nTop 10 by minutes:")
for r in sorted(rows, key=lambda r: -r[3])[:10]:
    print(f"  {r[0]} ({r[1]}, {r[2]}): {r[3]} min over {r[4]} seasons")