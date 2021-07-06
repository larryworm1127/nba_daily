"""Main App Views Module

@date: 06/02/2019
@author: Larry Shi
"""

from datetime import datetime

import requests
from dateutil import parser
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .forms import DateForm


# ==============================================================================
# Scores views
# ==============================================================================
def index(request):
    """Index page (with daily game scores).
    """
    date = datetime.today().date()
    return render_score_page(request, 'main/index.html', date, 'Home')


def score(request, date: str):
    """Scores page.
    """
    date_obj = parser.parse(date).date()
    return render_score_page(request, 'main/score.html', date_obj, date)


@csrf_protect
def render_score_page(request, page: str, date: datetime.date, title: str):
    """Render generic score page.
    """
    games = requests.get(f'http://{request.get_host()}/api/score/{date}').json()

    # Validate date input
    if request.method == 'POST':
        form = DateForm(request.POST)
        date_input = parser.parse(form.data.get('date')).date()

        if form.is_valid():
            return redirect('main:score', date=date_input.strftime("%m-%d-%Y"))

    context = {
        'title': title,
        'date': date.strftime("%b %d, %Y"),
        'games': games,
    }
    return render(request, page, context)


# ==============================================================================
# Players views
# ==============================================================================
def players(request, player_id):
    """Individual player stats page.
    """
    data = requests.get(f'http://{request.get_host()}/api/players/{player_id}').json()
    return render(request, 'main/players.html', data)


def players_game_log(request, player_id, season, season_type):
    """Individual player season game log page.
    """
    url = f'http://{request.get_host()}/api/players/{player_id}/{season}/{season_type}'
    data = requests.get(url).json()
    return render(request, 'main/player_games.html', context=data)


def players_stats(request):
    """Player list page.
    """
    data = requests.get(f'http://{request.get_host()}/api/player_list').json()
    return render(request, 'main/player_list.html', context={'data': data})


# ==============================================================================
# Teams views
# ==============================================================================
def teams(request, team_id):
    """Individual team detail page.
    """
    response = requests.get(f'http://{request.get_host()}/api/teams/{team_id}')
    return render(request, 'main/teams.html', context=response.json())


def team_game_log(request, team_id, season):
    """Individual team season game log page.
    """
    response = requests.get(f'http://{request.get_host()}/api/teams/{team_id}/{season}/Regular')
    return render(request, 'main/team_games.html', context=response.json())


def teams_stats(request):
    """Team list page.
    """
    response = requests.get(f'http://{request.get_host()}/api/team_list')
    context = {
        'data': response.json()
    }
    return render(request, 'main/teams_stats.html', context=context)


# ==============================================================================
# Games views
# ==============================================================================
def game_detail(request, game_id):
    """Single game box score page.
    """
    response = requests.get(f'http://{request.get_host()}/api/games/{game_id}')
    return render(request, 'main/game_detail.html', context=response.json())


# ==============================================================================
# Standing views
# ==============================================================================
def standings(request):
    """Season standing page.
    """
    response = requests.get(f'http://{request.get_host()}/api/standings')
    context = {
        'headers': [
            ('bg-danger', 'East Conference', 'East'),
            ('bg-primary', 'West Conference', 'West')
        ],
        'data': response.json()
    }
    return render(request, 'main/standings.html', context=context)
