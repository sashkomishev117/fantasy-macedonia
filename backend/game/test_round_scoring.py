from django.test import SimpleTestCase

from .round_scoring import team_round_points


class TeamRoundPointsTests(SimpleTestCase):
    def test_captain_counts_double(self):
        self.assertEqual(team_round_points({1: 5, 2: 3, 3: 2}, captain_id=1), 15)

    def test_no_captain(self):
        self.assertEqual(team_round_points({1: 5, 2: 3}, captain_id=None), 8)

    def test_captain_not_a_starter_gets_no_bonus(self):
        self.assertEqual(team_round_points({1: 5, 2: 3}, captain_id=9), 8)

    def test_negative_captain_hurts_twice(self):
        self.assertEqual(team_round_points({1: -2, 2: 4}, captain_id=1), 0)