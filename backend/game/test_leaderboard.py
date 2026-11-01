from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from .freeze import freeze_round
from .leaderboard import overall_ranking, round_ranking
from .models import FantasyTeam, Player, PlayerRoundStats, Round, SquadSlot, Team


class LeaderboardTests(TestCase):
    def setUp(self):
        club = Team.objects.create(id=1, name="Club")
        self.gk = Player.objects.create(id=1, team=club, name="Keeper", position="GK", price=20000)
        self.fwd = Player.objects.create(id=2, team=club, name="Striker", position="FWD", price=20000)
        User = get_user_model()

        # team A: the striker, who is captain
        self.a = FantasyTeam.objects.create(
            owner=User.objects.create_user("a", password="pw"), name="Team A", captain=self.fwd
        )
        SquadSlot.objects.create(team=self.a, player=self.fwd, is_starter=True)

        # team B: the keeper only
        self.b = FantasyTeam.objects.create(
            owner=User.objects.create_user("b", password="pw"), name="Team B"
        )
        SquadSlot.objects.create(team=self.b, player=self.gk, is_starter=True)

        round_ = Round.objects.create(number=1, deadline=timezone.now() - timedelta(hours=1))
        PlayerRoundStats.objects.create(round=round_, player=self.fwd, minutes=90, goals=1)  # 6 points
        PlayerRoundStats.objects.create(round=round_, player=self.gk, minutes=30, goals_conceded=1)  # 1 point
        freeze_round(round_)
        self.round = Round.objects.get(number=1)

    def test_round_ranking_order_and_points(self):
        ranking = round_ranking(self.round)
        self.assertEqual([r["name"] for r in ranking], ["Team A", "Team B"])
        self.assertEqual([r["points"] for r in ranking], [12, 1])   # captain doubles 6
        self.assertEqual([r["rank"] for r in ranking], [1, 2])

    def test_overall_ranking_adds_frozen_rounds(self):
        ranking = overall_ranking()
        self.assertEqual([r["points"] for r in ranking], [12, 1])

    def test_unfrozen_rounds_are_not_in_the_overall_total(self):
        Round.objects.create(number=2, deadline=timezone.now() + timedelta(days=1))
        self.assertEqual([r["points"] for r in overall_ranking()], [12, 1])