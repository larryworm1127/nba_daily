"""Main App Admin Control Module

@date: 06/02/2019
@author: Larry Shi
"""
from django.contrib import admin

from .models import Player, Team, TeamGameLog, PlayerGameLog, Game


# ------------------------------------------------------------------------------
# Register models
# ------------------------------------------------------------------------------
class PlayerAdmin(admin.ModelAdmin):
    search_fields = (
        'first_name', 'last_name', 'player_id',
        'team__team_name',
    )


class TeamAdmin(admin.ModelAdmin):
    search_fields = (
        'team_name', 'team_city', 'team_id',
    )


class TeamGameLogAdmin(admin.ModelAdmin):
    search_fields = (
        'team__team_name', 'team__team_city', 'team__team_id'
    )


class PlayerGameLogAdmin(admin.ModelAdmin):
    search_fields = (
        'player__first_name', 'player__last_name', 'player__player_id'
    )


class GameAdmin(admin.ModelAdmin):
    search_fields = (
        'game_id',
    )


admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamGameLog, TeamGameLogAdmin)
admin.site.register(PlayerGameLog, PlayerGameLogAdmin)
admin.site.register(Game, GameAdmin)
