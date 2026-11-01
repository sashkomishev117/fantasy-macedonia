from .models import PlayerRoundStats, RoundSquad


def team_round_points(starter_points, captain_id):
    """starter_points: {player_id: points} for the starting 11.
    The captain counts double."""
    total = sum(starter_points.values())
    if captain_id in starter_points:
        total += starter_points[captain_id]
    return total


def compute_team_round_points(team, round_):
    stats = {
        s.player_id: s.points
        for s in PlayerRoundStats.objects.filter(round=round_)
    }

    if round_.is_frozen:
        # use the squad as it was at the deadline
        squad = RoundSquad.objects.filter(team=team, round=round_).first()
        if squad is None:
            return 0          # the team had no squad at the deadline
        starter_ids = squad.slots.filter(is_starter=True).values_list("player_id", flat=True)
        captain_id = squad.captain_id
    else:
        # round still open: a preview using the current squad
        starter_ids = team.slots.filter(is_starter=True).values_list("player_id", flat=True)
        captain_id = team.captain_id

    starter_points = {pid: stats.get(pid, 0) for pid in starter_ids}
    return team_round_points(starter_points, captain_id)