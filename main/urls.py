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
    path('players/', views.player_list, name='player_list'),
    path('players/<str:player_id>/', views.players, name='players'),
    path('players/<str:player_id>/<str:season>', views.player_games, name='player_games')
]

# Teams pages URL
urlpatterns += [
    path('teams/', views.team_list, name='team_list'),
    path('teams/<str:team_id>/', views.teams, name='teams'),
    path('teams/<str:team_id>/<str:season>', views.teams, name='team_games'),
    path('standing/', views.standing, name='standing')
]

# Games page URL
urlpatterns += [
    path('games/<str:game_id>', views.box_score, name='boxscore'),
]
