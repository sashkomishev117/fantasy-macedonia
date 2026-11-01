from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import permissions, serializers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FantasyTeam, Player, SquadSlot
from .serializers import PlayerSerializer
from .squad import validate_squad

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = str(request.data.get("username", "")).strip()
        password = str(request.data.get("password",""))
        if not username or len(password) < 8:
            return Response(
                {"errors" : ["Username is required and the password needst 8+ characters"]}, status=400,
            )
        User = get_user_model()
        if User.objects.filter(username__iexact=username).exists():
            return Response(
                {"errors" : ["That username is taken."]}, status=400,
            )
        user = User.objects.create_user(username=username, password=password)
        FantasyTeam.objects.create(owner=user, name=f"{username}'s team")
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=201)

class SquadInputSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=False)
    players = serializers.ListField(child=serializers.IntegerField())
    starters = serializers.ListField(child=serializers.IntegerField())
    captain = serializers.IntegerField(allow_null=True, required=False)

class SquadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_team(self, user):
        team, _ = FantasyTeam.objects.get_or_create(
            owner=user, defaults={"name": f"{user.username}'s team"}
        )
        return team

    def render(self, team):
        slots = list(team.slots.select_related("player__team"))
        spent = sum(s.player.price or 0 for s in slots)
        return {
            "name": team.name,
            "budget": team.budget,
            "spent": spent,
            "remaining": team.budget - spent,
            "captain": team.captain_id,
            "players": [
                {**PlayerSerializer(s.player).data, "is_starter": s.is_starter}
                for s in slots
            ],
        }

    def get(self, request):
        return Response(self.render(self.get_team(request.user)))

    def put(self, request):
        team = self.get_team(request.user)
        ser = SquadInputSerializer(data=request.data)
        ser.is_valid(raise_exception=True)
        data = ser.validated_data

        ids = data["players"]
        found = {p.id: p for p in Player.objects.filter(id__in=ids)}
        missing = [i for i in ids if i not in found]
        if missing:
            return Response({"errors": [f"Unknown player ids: {missing}"]}, status=400)

        players = [found[i] for i in ids]
        starter_ids = set(data["starters"])
        captain = data.get("captain")

        errors = validate_squad(players, starter_ids, team.budget, captain)
        if errors:
            return Response({"errors": errors}, status=400)

        with transaction.atomic():
            team.slots.all().delete()
            SquadSlot.objects.bulk_create(
                SquadSlot(team=team, player=p, is_starter=p.id in starter_ids)
                for p in players
            )
            team.captain = found.get(captain)
            if "name" in data:
                team.name = data["name"]
            team.save()

        return Response(self.render(team))