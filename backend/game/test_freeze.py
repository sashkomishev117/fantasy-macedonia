from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from .freeze import freeze_due_rounds, freeze_round
from .models import FantasyTeam, Player, PlayerRoundStats, Round, RoundSquad, SquadSlot, Team
from .round_scoring import compute_team_round_points


class FreezeTests(TestCase):
    def setUp(self):
        club = Team.objects.create(id=1, name="Club")
        self.gk = Player.objects.create(id=1, team=club, name="Keeper", position="GK", price=20000)
        self.fwd = Player.objects.create(id=2, team=club, name="Striker", position="FWD", price=20000)
        user = get_user_model().objects.create_user("u1", password="pw")
        self.team = FantasyTeam.objects.create(owner=user, name="T1", captain=self.fwd)
        SquadSlot.objects.create(team=self.team, player=self.gk, is_starter=True)
        SquadSlot.objects.create(team=self.team, player=self.fwd, is_starter=True)
        self.round = Round.objects.create(number=1, deadline=timezone.now() - timedelta(hours=1))

    def test_due_round_is_frozen(self):
        freeze_due_rounds()
        self.round.refresh_from_db()
        self.assertTrue(self.round.is_frozen)
        self.assertEqual(RoundSquad.objects.filter(round=self.round).count(), 1)

    def test_future_round_is_not_frozen(self):
        future = Round.objects.create(number=2, deadline=timezone.now() + timedelta(days=1))
        freeze_due_rounds()
        future.refresh_from_db()
        self.assertFalse(future.is_frozen)

    def test_freezing_twice_is_safe(self):
        freeze_round(self.round)
        freeze_round(self.round)
        self.assertEqual(RoundSquad.objects.filter(round=self.round).count(), 1)

    def test_points_use_the_frozen_squad(self):
        PlayerRoundStats.objects.create(round=self.round, player=self.fwd, minutes=90, goals=1)
        freeze_round(self.round)
        self.round.refresh_from_db()
        # the user changes the squad after the deadline
        self.team.slots.filter(player=self.fwd).delete()
        self.team.captain = None
        self.team.save()
        # 90 min (2) + goal (4) = 6, captain doubles it: 12
        self.assertEqual(compute_team_round_points(self.team, self.round), 12)

    def test_team_with_no_squad_at_the_deadline_scores_zero(self):
        PlayerRoundStats.objects.create(round=self.round, player=self.fwd, minutes=90, goals=1)
        freeze_round(self.round)
        self.round.refresh_from_db()
        late_user = get_user_model().objects.create_user("u2", password="pw")
        late = FantasyTeam.objects.create(owner=late_user, name="T2", captain=self.fwd)
        SquadSlot.objects.create(team=late, player=self.fwd, is_starter=True)
        self.assertEqual(compute_team_round_points(late, self.round), 0)