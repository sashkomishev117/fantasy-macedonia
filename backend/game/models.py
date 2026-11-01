from django.db import models
from django.conf import settings

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
    