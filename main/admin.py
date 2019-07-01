"""Main App Admin Control Module

@date: 06/02/2019
@author: Larry Shi
"""
from django.contrib import admin

from .models import Player, Team, TeamGameLog, PlayerGameLog, Game

# Register models
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(TeamGameLog)
admin.site.register(PlayerGameLog)
admin.site.register(Game)
