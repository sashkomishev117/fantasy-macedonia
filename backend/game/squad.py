from collections import Counter

SQUAD_COMPOSITION = {"GK": 2, "DEF": 5, "MID": 5, "FWD": 3}
MIN_STARTERS = {"GK": 1, "DEF": 3, "MID": 2, "FWD": 1}
STARTERS = 11
MAX_PER_CLUB = 3

def validate_squad(players, starter_ids, budget, captain_id=None):
    errors = []

    if len({p.id for p in players}) != len(players):
        errors.append("A player is in the squad more than once")

    counts = Counter(p.position for p in players)
    if len(players) != sum(SQUAD_COMPOSITION.values()) or counts != Counter(SQUAD_COMPOSITION):
        errors.append(f"Squad must have 2 GKs, 5 DEFs, 5 MIDs, and 3 FWDs (got {dict(counts)})")

    for club, n in Counter(p.team_id for p in players).items():
        if n > MAX_PER_CLUB:
            errors.append(f"Too many players from {club} ({n} > {MAX_PER_CLUB})")
            break

    if any(p.price is None for p in players):
        errors.append("Some players have no price set")
    else:
        total = sum(p.price for p in players)
        if total > budget:
            errors.append(f"Squad costs {total:,} MKD, which exceeds the budget of {budget:,} MKD")

    # starting 11

    ids = {p.id for p in players}
    if not starter_ids <= ids:
        errors.append("Some starters are not in the squad")
    starters = [p for p in players if p.id in starter_ids]
    start_counts = Counter(p.position for p in starters)
    if len(starters) != STARTERS:
        errors.append(f"Pick exactly {STARTERS} starters (got {len(starters)})")

    for pos, minimum in MIN_STARTERS.items():
        if start_counts[pos] < minimum:
            errors.append(f"Pick at least {minimum} {pos} starters (got {start_counts[pos]})")
    if start_counts["GK"] > 1:
        errors.append("Only one goalkeeper can start")

    # captain must be one of the starters
    if captain_id is not None and captain_id not in starter_ids:
        errors.append("Captain must be one of the starters")

    return errors