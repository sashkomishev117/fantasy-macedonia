from .models import PlayerRoundStats

def team_round_points(starter_points, captain_id):
    total = sum(starter_points.values())
    if captain_id in starter_points:
        total+= starter_points[captain_id]
    return total

def compute_team_round_points(team, round_):
    stats = {
        s.player_id: s.points
        for s in PlayerRoundStats.objects.filter(round=round_)
    }
    starter_ids = team.slots.filter(is_starter=True).values_list("player_id", flat=True)
    starter_points = {pid: stats.get(pid, 0) for pid in starter_ids}

    return team_round_points(starter_points, team.captain_id)

