"""Main App Admin Control Module

@date: 06/02/2019
@author: Larry Shi
"""
from django.contrib import admin

from .models import Player, Team

# Register models
admin.site.register(Player)
admin.site.register(Team)
