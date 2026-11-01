from django.test import SimpleTestCase

from .scoring import calculate_points


class CalculatePointsTests(SimpleTestCase):
    def test_did_not_play(self):
        self.assertEqual(calculate_points("FWD", 0, goals=1), 0)

    def test_short_substitute_appearance(self):
        self.assertEqual(calculate_points("MID", 30, goals_conceded=1), 1)

    def test_full_match_no_events(self):
        self.assertEqual(calculate_points("MID", 90, goals_conceded=1), 2)

    def test_defender_clean_sheet(self):
        self.assertEqual(calculate_points("DEF", 90), 6)

    def test_clean_sheet_needs_sixty_minutes(self):
        self.assertEqual(calculate_points("DEF", 45), 1)

    def test_midfielder_clean_sheet(self):
        self.assertEqual(calculate_points("MID", 90), 3)

    def test_goalkeeper_concedes_three(self):
        self.assertEqual(calculate_points("GK", 90, goals_conceded=3), 1)

    def test_forward_goal_and_assist(self):
        self.assertEqual(calculate_points("FWD", 90, goals=1, assists=1, goals_conceded=1), 9)

    def test_yellow_and_red_card(self):
        self.assertEqual(
            calculate_points("MID", 70, goals_conceded=1, yellow_cards=1, red_card=True), -2
        )