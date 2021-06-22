"""API App URL Module

@date: 06/20/2021
@author: Larry Shi
"""
from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('standings/', views.standings_api, name='standings-api'),
]
