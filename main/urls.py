from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('players/<int:player_id>/', views.players, name='players'),
    path('teams/<int:team_id>/', views.teams, name='teams')
]
