"""Main App Views Module

@date: 06/02/2019
@author: Larry Shi
"""

from datetime import datetime

import requests
from dateutil import parser
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_protect

from .forms import DateForm
from .models import (
    Player,
    Team,
    Game,
    TeamGameLog,
    PlayerGameLog
)


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
        'closest_date': Game.get_closest_game_date(date).strftime("%m-%d-%Y")
    }
    return render(request, page, context)


# ==============================================================================
# Players views
# ==============================================================================
def players(request, team_id: int):
    """Individual player stats page.
    """
    data = requests.get(f'http://{request.get_host()}/api/players/{team_id}').json()
    return render(request, 'main/players.html', data)


class PlayerGamesListView(generic.ListView):
    """Individual player season game log page.
    """
    model = PlayerGameLog
    template_name = 'main/player_games.html'

    def get_queryset(self):
        """Return desired queryset to be displayed.
        """
        return PlayerGameLog.objects.filter(player=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        """Return the updated context data.
        """
        context = super(PlayerGamesListView, self).get_context_data(**kwargs)
        context['player'] = get_object_or_404(Player, pk=self.kwargs['pk'])
        return context


class PlayerListView(generic.ListView):
    """Player list page.
    """
    model = Player
    paginate_by = 20


# ==============================================================================
# Teams views
# ==============================================================================
class TeamGamesListView(generic.ListView):
    """Individual team season game log page.
    """
    model = TeamGameLog
    template_name = 'main/team_games.html'

    def get_queryset(self):
        """Return desired queryset to be displayed.
        """
        return TeamGameLog.objects.filter(team=self.kwargs['pk'])

    def get_context_data(self, *, object_list=None, **kwargs):
        """Return the updated context data.
        """
        context = super(TeamGamesListView, self).get_context_data(**kwargs)
        context['team'] = get_object_or_404(Team, pk=self.kwargs['pk'])
        return context


def teams(request, team_id):
    """Individual team detail page.
    """
    response = requests.get(f'http://{request.get_host()}/api/teams/{team_id}')
    return render(request, 'main/teams.html', context=response.json())


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
