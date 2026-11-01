from types import SimpleNamespace

from django.test import SimpleTestCase

from .squad import validate_squad

POSITIONS = ["GK"] * 2 + ["DEF"] * 5 + ["MID"] * 5 + ["FWD"] * 3
STARTERS = {0, 2, 3, 4, 5, 7, 8, 9, 10, 12, 13}   # 1 GK, 4 DEF, 4 MID, 2 FWD


def make_squad(price=20_000):
    # 15 players spread over 5 clubs, 3 per club
    return [SimpleNamespace(id=i, position=pos, team_id=i % 5, price=price)
            for i, pos in enumerate(POSITIONS)]


class ValidateSquadTests(SimpleTestCase):
    def test_valid_squad(self):
        self.assertEqual(validate_squad(make_squad(), STARTERS, 700_000, captain_id=12), [])

    def test_over_budget(self):
        self.assertTrue(validate_squad(make_squad(price=60_000), STARTERS, 700_000))

    def test_too_many_from_one_club(self):
        squad = make_squad()
        for p in squad[:4]:
            p.team_id = 99
        self.assertTrue(validate_squad(squad, STARTERS, 700_000))

    def test_wrong_composition(self):
        squad = make_squad()
        squad[14].position = "DEF"
        self.assertTrue(validate_squad(squad, STARTERS, 700_000))

    def test_two_starting_goalkeepers(self):
        self.assertTrue(validate_squad(make_squad(), (STARTERS - {12}) | {1}, 700_000))

    def test_captain_on_bench(self):
        self.assertTrue(validate_squad(make_squad(), STARTERS, 700_000, captain_id=6))