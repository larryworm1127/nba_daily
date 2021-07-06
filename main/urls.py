"""Main App URL Module

@date: 06/02/2019
@author: Larry Shi
"""
from django.urls import path

from . import views

app_name = 'main'

# Score/Index pages URL
urlpatterns = [
    path('', views.index, name='index'),
    path('score/<str:date>', views.score, name='score')
]

# Players pages URL
urlpatterns += [
    path('players/', views.PlayerListView.as_view(), name='player_list'),
    path('players/<int:player_id>/', views.players, name='players'),
    path('players/<int:player_id>/<str:season>/<str:season_type>', views.players_game_log, name='player_games')
]

# Teams pages URL
urlpatterns += [
    path('teams/', views.teams_stats, name='team_list'),
    path('teams/<int:team_id>/', views.teams, name='teams'),
    path('teams/<int:team_id>/<str:season>', views.team_game_log, name='team_games'),
    path('standings/', views.standings, name='standing')
]

# Games page URL
urlpatterns += [
    path('games/<str:game_id>', views.game_detail, name='boxscore'),
]
