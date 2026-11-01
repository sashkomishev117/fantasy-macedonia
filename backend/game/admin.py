from django.contrib import admin

from .models import FantasyTeam, Player, PlayerRoundStats, Round, SquadSlot, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "id")


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "position", "price", "market_value")
    list_filter = ("team", "position")
    search_fields = ("name",)
    ordering = ("-price",)


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ("number", "deadline", "is_finished")


@admin.register(PlayerRoundStats)
class PlayerRoundStatsAdmin(admin.ModelAdmin):
    list_display = ("player", "round", "minutes", "goals", "assists", "points")
    list_filter = ("round", "player__team")
    autocomplete_fields = ["player"]
    readonly_fields = ("points",)


admin.site.register(FantasyTeam)
admin.site.register(SquadSlot)