"""Main App URL Module

@date: 06/02/2019
@author: Larry Shi
"""
from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('score/<str:date>', views.score, name='score'),
    path('players/', views.player_list, name='player_list'),
    path('players/<str:player_id>/', views.players, name='players'),
    path('teams/', views.team_list, name='team_list'),
    path('teams/<str:team_id>/', views.teams, name='teams'),
    path('games/<str:game_id>', views.box_score, name='boxscore'),
    path('standing/', views.standing, name='standing')
]
