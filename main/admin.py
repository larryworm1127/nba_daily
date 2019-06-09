from django.contrib import admin

from .models import Player, Team

# Register models
admin.site.register(Player)
admin.site.register(Team)
