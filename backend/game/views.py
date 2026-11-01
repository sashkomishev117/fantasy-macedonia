from rest_framework import filters, generics

from .models import Player, Team
from .serializers import PlayerSerializer, TeamSerializer


class TeamList(generics.ListAPIView):
    queryset = Team.objects.order_by("name")
    serializer_class = TeamSerializer
    pagination_class = None


class PlayerList(generics.ListAPIView):
    """All players. Filters: ?position=GK|DEF|MID|FWD, ?team=<club id>,
    ?search=<name>, ?ordering=price or ?ordering=-price"""

    serializer_class = PlayerSerializer
    pagination_class = None
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["price", "name", "market_value"]
    ordering = ["-price"]

    def get_queryset(self):
        qs = Player.objects.select_related("team")
        position = self.request.query_params.get("position")
        team = self.request.query_params.get("team")
        if position:
            qs = qs.filter(position=position.upper())
        if team:
            qs = qs.filter(team_id=team)
        return qs


class PlayerDetail(generics.RetrieveAPIView):
    queryset = Player.objects.select_related("team")
    serializer_class = PlayerSerializer
