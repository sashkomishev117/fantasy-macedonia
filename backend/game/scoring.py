GOAL_POINTS = {"GK": 6, "DEF": 6, "MID": 5, "FWD": 4}
CLEAN_SHEET_POINTS = {"GK": 4, "DEF": 4, "MID": 1, "FWD": 0}
ASSIST_POINTS = 3
YELLOW_POINTS = -1
RED_POINTS = -3


def calculate_points(
    position,
    minutes,
    goals=0,
    assists=0,
    goals_conceded=0,
    yellow_cards=0,
    red_card=False,
):
    """Fantasy points for one player in one match.

    goals_conceded is the number of goals his team conceded in the match.
    """
    if minutes <= 0:
        return 0

    points = 2 if minutes >= 60 else 1
    points += goals * GOAL_POINTS[position]
    points += assists * ASSIST_POINTS

    if minutes >= 60 and goals_conceded == 0:
        points += CLEAN_SHEET_POINTS[position]

    if position in ("GK", "DEF"):
        points -= goals_conceded // 2

    points += yellow_cards * YELLOW_POINTS
    if red_card:
        points += RED_POINTS

    return points