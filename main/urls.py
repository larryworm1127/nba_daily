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
    path('players/<int:pk>/', views.players, name='players'),
    path('players/<int:pk>/<str:season>', views.PlayerGamesListView.as_view(), name='player_games')
]

# Teams pages URL
urlpatterns += [
    path('teams/', views.TeamListView.as_view(), name='team_list'),
    path('teams/<int:pk>/', views.TeamDetailView.as_view(), name='teams'),
    path('teams/<int:pk>/<str:season>', views.TeamGamesListView.as_view(), name='team_games'),
    # path('standing/', views.StandingListView.as_view(), name='standing'),
    path('standings/', views.standings, name='standing')
]

# Games page URL
urlpatterns += [
    path('games/<str:pk>', views.GameDetailView.as_view(), name='boxscore'),
]
