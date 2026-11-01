from .models import FantasyTeam, Round
from .round_scoring import compute_team_round_points


def _rank(rows):
    rows.sort(key=lambda r: (-r["points"], r["name"].lower()))
    for place, row in enumerate(rows, 1):
        row["rank"] = place
    return rows


def _teams():
    return FantasyTeam.objects.select_related("owner")


def round_ranking(round_):
    rows = [
        {
            "team_id": t.id,
            "name": t.name,
            "username": t.owner.username,
            "points": compute_team_round_points(t, round_),
        }
        for t in _teams()
    ]
    return _rank(rows)


def overall_ranking():
    rounds = list(Round.objects.filter(is_frozen=True))
    rows = [
        {
            "team_id": t.id,
            "name": t.name,
            "username": t.owner.username,
            "points": sum(compute_team_round_points(t, r) for r in rounds),
        }
        for t in _teams()
    ]
    return _rank(rows)