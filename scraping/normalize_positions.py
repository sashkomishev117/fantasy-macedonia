import csv
from collections import Counter

GROUPS = {
    "Goalkeeper": "Goalkeeper",
    "Centre-Back": "Defender",
    "Left-Back": "Defender",
    "Right-Back": "Defender",
    "Defender": "Defender",
    "Defensive Midfield": "Midfielder",
    "Central Midfield": "Midfielder",
    "Attacking Midfield": "Midfielder",
    "Midfield": "Midfielder",
    "Left Winger": "Forward",
    "Right Winger": "Forward",
    "Second Striker": "Forward",
    "Centre-Forward": "Forward",
}

with open("mk_first_league.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    fieldnames = list(reader.fieldnames)
    rows = list(reader)

# keep the original detailed position the first time we run
if "position_detail" not in fieldnames:
    fieldnames.insert(fieldnames.index("position") + 1, "position_detail")
    for row in rows:
        row["position_detail"] = row["position"]

unknown = {r["position_detail"] for r in rows if r["position_detail"] not in GROUPS}
if unknown:
    raise SystemExit(f"Unmapped positions, add them to GROUPS: {unknown}")

for row in rows:
    row["position"] = GROUPS[row["position_detail"]]

with open("mk_first_league.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

print(Counter(r["position"] for r in rows))
