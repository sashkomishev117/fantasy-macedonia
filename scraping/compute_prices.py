import csv
import json
import statistics

LEAGUE = "MAZ1"
WEIGHTS = {"2026": 1.0, "2025": 1.0, "2024": 0.75, "2023": 0.5, "2022": 0.25}
K = 8                # prior strength, in 90-minute games
NO_HISTORY = 0.6    # players with no league minutes get 85% of the position average
FLOOR, CAP = 20_000, 100_000

GOAL = {"Goalkeeper": 6, "Defender": 6, "Midfielder": 5, "Forward": 4}
CLEAN_SHEET = {"Goalkeeper": 4, "Defender": 4, "Midfielder": 1, "Forward": 0}
CONCEDED = {"Goalkeeper": -0.5, "Defender": -0.5, "Midfielder": 0, "Forward": 0}
NEED = {"Goalkeeper": 2, "Defender": 5, "Midfielder": 5, "Forward": 3}


def season_points(s, pos):
    v = lambda key: s[key] or 0
    games = v("minutes_played") / 90
    # team results are counted while he's in the squad, so cap them by his playing time
    clean_sheets = min(v("clean_sheets"), games * 0.5)
    conceded = min(v("goals_conceded"), games * 2)
    return (
        v("minutes_played") / 45
        + v("goals") * GOAL[pos]
        + v("assists") * 3
        + clean_sheets * CLEAN_SHEET[pos]
        + conceded * CONCEDED[pos]
        - v("yellow_cards")
        - 3 * (v("red_cards") + v("second_yellow_cards"))
    )

with open("mk_first_league.csv", encoding="utf-8") as f:
    players = list(csv.DictReader(f))
with open("stats_raw.json", encoding="utf-8") as f:
    stats = json.load(f)

# 1. weighted points and minutes per player (league only, last five seasons)
for p in players:
    pts = mins = 0.0
    for s in stats.get(p["id"], []):
        w = WEIGHTS.get(s["season_id"])
        if s["competition_id"] != LEAGUE or w is None:
            continue
        pts += w * season_points(s, p["position"])
        mins += w * (s["minutes_played"] or 0)
    p["w_pts"], p["w_min"] = pts, mins

# 2. position averages (points per 90)
prior = {}
for pos in NEED:
    group = [p for p in players if p["position"] == pos]
    prior[pos] = sum(p["w_pts"] for p in group) / sum(p["w_min"] for p in group) * 90
print("Position averages (points per 90):", {k: round(v, 2) for k, v in prior.items()})

# 3. shrunk estimate per player
for p in players:
    pos = p["position"]
    n = p["w_min"] / 90
    if n == 0:
        p["est"] = prior[pos] * NO_HISTORY
    else:
        p["est"] = (p["w_pts"] + K * prior[pos]) / (n + K)

# 4. estimate -> price, measured above a replacement-level player
ests = sorted(p["est"] for p in players)
REPL = ests[int(len(ests) * 0.10)]        # roughly the 10th-percentile player costs FLOOR
hi = ests[-1]  
for p in players:
    x = max(0.0, p["est"] - REPL) / (hi - REPL)
    raw = FLOOR + x * (CAP - FLOOR)
    p["price"] = int(round(min(CAP, raw) / 5000) * 5000)

with open("prices.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["id", "name", "team", "position", "est_per90", "price"])
    for p in players:
        w.writerow([p["id"], p["name"], p["team"], p["position"], round(p["est"], 2), p["price"]])

# 5. sanity checks and a suggested budget
prices = [p["price"] for p in players]
print("Prices min/median/mean/max:", min(prices), statistics.median(prices),
      round(statistics.mean(prices)), max(prices))

cheapest = priciest = 0
for pos, n in NEED.items():
    ps = sorted(p["price"] for p in players if p["position"] == pos)
    cheapest += sum(ps[:n])
    priciest += sum(ps[-n:])
budget = round(cheapest / 0.575 / 50_000) * 50_000
print(f"Cheapest legal squad: {cheapest} | priciest squad: {priciest}")
print(f"Suggested budget: {budget} (cheapest = {cheapest / budget:.0%} of it, "
      f"priciest = {priciest / budget:.0%})")

print("\nTop 15:")
for p in sorted(players, key=lambda p: -p["price"])[:15]:
    print(f"  {p['price']:>7}  {p['name']} ({p['team']}, {p['position']}, {round(p['est'], 2)}/90)")

print("\nCheapest regulars (3000+ weighted minutes):")
regulars = [p for p in players if p["w_min"] >= 3000]
for p in sorted(regulars, key=lambda p: p["price"])[:8]:
    print(f"  {p['price']:>7}  {p['name']} ({p['team']}, {p['position']}, {round(p['est'], 2)}/90)")
