from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('players/', views.player_list, name='player_list'),
    path('players/<int:player_id>/', views.players, name='players'),
    path('teams/', views.team_list, name='team_list'),
    path('teams/<int:team_id>/', views.teams, name='teams')
]
