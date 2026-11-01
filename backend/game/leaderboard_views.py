from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .freeze import freeze_due_rounds
from .leaderboard import overall_ranking, round_ranking
from .models import Round


class LeaderboardView(APIView):
    """GET /api/leaderboard/            overall ranking (frozen rounds only)
    GET /api/leaderboard/?round=<n>     ranking for one round"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        freeze_due_rounds()
        number = request.query_params.get("round")
        if number is None:
            return Response({"round": None, "ranking": overall_ranking()})

        try:
            round_ = Round.objects.get(number=int(number))
        except (ValueError, Round.DoesNotExist):
            return Response({"errors": ["Unknown round."]}, status=404)

        return Response({
            "round": round_.number,
            "is_frozen": round_.is_frozen,
            "is_finished": round_.is_finished,
            "ranking": round_ranking(round_),
        })