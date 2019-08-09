"""Main App Admin Control Module

@date: 06/02/2019
@author: Larry Shi
"""
from django.contrib import admin

from .models import (
    Player,
    Team,
    TeamGameLog,
    PlayerGameLog,
    Game,
    TeamSeasonStats,
    PlayerSeasonStats,
    Standing,
    PlayerCareerStats)


# ------------------------------------------------------------------------------
# Register models
# ------------------------------------------------------------------------------
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    search_fields = (
        'first_name', 'last_name', 'player_id',
        'team__team_name',
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = (
        'team_name', 'team_city', 'team_id',
    )


@admin.register(TeamGameLog)
class TeamGameLogAdmin(admin.ModelAdmin):
    search_fields = (
        'team__team_name', 'team__team_city', 'team__team_id'
    )


@admin.register(PlayerGameLog)
class PlayerGameLogAdmin(admin.ModelAdmin):
    search_fields = (
        'player__first_name', 'player__last_name', 'player__player_id'
    )


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    search_fields = (
        'game_id',
    )


@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    search_fields = (
        'team__team_name', 'team__team_city', 'team__team_id'
    )


@admin.register(TeamSeasonStats)
class TeamSeasonStatsAdmin(admin.ModelAdmin):
    search_fields = (
        'team__team_name', 'team__team_city', 'team__team_id'
    )


@admin.register(PlayerSeasonStats)
class PlayerSeasonStatsAdmin(admin.ModelAdmin):
    search_fields = (
        'player__last_name', 'player__first_name', 'player__player_id', 'season'
    )


@admin.register(PlayerCareerStats)
class PlayerCareerStatsAdmin(admin.ModelAdmin):
    search_fields = (
        'player__last_name', 'player__first_name', 'player__player_id', 'season'
    )
