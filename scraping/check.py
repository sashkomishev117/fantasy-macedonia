import csv

with open("mk_first_league.csv", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

missing = [r for r in rows if not r["position"]]
print(len(missing), "players without a position")
for r in missing:
    print(r["id"], r["name"], "-", r["team"])