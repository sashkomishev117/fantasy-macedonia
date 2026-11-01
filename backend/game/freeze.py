from django.db import transaction
from django.utils import timezone

from .models import FantasyTeam, Round, RoundSquad, RoundSquadSlot

@transaction.atomic
def freeze_round(round_):
    if round_.is_frozen:
        return 0

    saved = 0
    for team in FantasyTeam.objects.prefetch_related("slots"):
        slots = list(team.slots.all())
        if not slots:
            continue
        squad, created = RoundSquad.objects.get_or_create(
            team=team, round=round_, defaults={"captain_id": team.captain_id}
        )
        if created:
            RoundSquadSlot.objects.bulk_create(
                RoundSquadSlot(squad=squad, player_id=s.player_id, is_starter=s.is_starter) for s in slots
            )
            saved += 1

        round_.is_frozen = True
        round_.save(update_fields=["is_frozen"])
        return saved

def freeze_due_rounds(now=None):
    now = now or timezone.now()
    for round_ in Round.objects.filter(is_frozen=False, deadline__lte=now):
        freeze_round(round_)