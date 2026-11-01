from rest_framework import serializers

from .models import Player, Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ["id", "name"]


class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source="team.name", read_only=True)

    class Meta:
        model = Player
        fields = [
            "id", "name", "team", "team_name", "position", "position_detail",
            "shirt_number", "date_of_birth", "nationality", "height", "foot",
            "market_value", "price",
        ]
