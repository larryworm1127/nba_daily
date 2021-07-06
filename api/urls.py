"""API App URL Module

@date: 06/20/2021
@author: Larry Shi
"""
from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('standings/', views.standings_api),
    path('team_list/', views.team_list_api),
    path('score/<str:date>', views.game_by_date_api),
    path('games/<str:game_id>', views.game_by_id_api),
    path('teams/<str:team_id>', views.team_detail_api),
    path('teams/<str:team_id>/<str:season>/<str:season_type>', views.team_game_log_api),
    path('players/<str:player_id>', views.player_detail_api),
    path('players/<str:player_id>/<str:season>/<str:season_type>', views.player_game_log_api)
]
