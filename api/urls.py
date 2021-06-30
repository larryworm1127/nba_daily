"""API App URL Module

@date: 06/20/2021
@author: Larry Shi
"""
from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('standings/', views.standings_api, name='standings-api'),
    path('team_list/', views.team_list_api, name='team-list-api'),
    path('score/<str:date>', views.game_by_date_api, name='game-by-date-api'),
    path('games/<str:game_id>', views.game_by_id_api, name='game-by-id-api'),
    path('teams/<str:team_id>', views.team_detail_api, name='team-detail-api'),
    path('players/<str:player_id>', views.player_detail_api, name='player-detail-api'),
]
