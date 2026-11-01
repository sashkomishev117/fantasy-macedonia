from django.db import models
from django.conf import settings
from .scoring import calculate_points

# Create your models here.

class Team(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Player(models.Model):
    class Position(models.TextChoices):
        GOALKEEPER = "GK", "Goalkeeper"
        DEFENDER = "DEF", "Defender"
        MIDFIELDER = "MID", "Midfielder"
        FORWARD = "FWD", "Forward"

    id = models.PositiveIntegerField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=3, choices=Position.choices)
    position_detail = models.CharField(max_length=30, blank=True)
    shirt_number = models.PositiveSmallIntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=200, blank=True)
    height = models.PositiveSmallIntegerField(null=True, blank=True)
    foot = models.CharField(max_length=10, blank=True)
    market_value = models.PositiveIntegerField(null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.team})"

class FantasyTeam(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="fantasy_team")
    name = models.CharField(max_length=50)
    budget = models.PositiveIntegerField(default=700_000)
    captain = models.ForeignKey(Player, null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    def __str__(self):
        return self.name

class SquadSlot(models.Model):
    team = models.ForeignKey(FantasyTeam, on_delete=models.CASCADE, related_name="slots")
    player = models.ForeignKey(Player, on_delete=models.PROTECT, related_name="+")
    is_starter = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["team", "player"], name="unique_player_per_team")
        ]

class Round(models.Model):
    number = models.PositiveSmallIntegerField(unique=True)
    deadline = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Round {self.number}"

class PlayerRoundStats(models.Model):
    round = models.ForeignKey(Round, on_delete=models.CASCADE, related_name="stats")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="round_stats")
    minutes = models.PositiveSmallIntegerField(default = 0)
    goals = models.PositiveSmallIntegerField(default = 0)
    assists = models.PositiveSmallIntegerField(default = 0)
    goals_conceded = models.PositiveSmallIntegerField(default = 0)
    yellow_cards = models.PositiveSmallIntegerField(default = 0)
    red_card = models.BooleanField(default = False)
    points = models.IntegerField(default = 0, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["round", "player"], name="unique_player_per_round")
        ]

    def save(self, *args, **kwargs):
        self.points = calculate_points(
            self.player.position,
            self.minutes,
            self.goals,
            self.assists,
            self.goals_conceded,
            self.yellow_cards,
            self.red_card,
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.player} in {self.round}: {self.points} points"