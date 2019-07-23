"""Main App Views Module

@date: 06/02/2019
@author: Larry Shi
"""

from datetime import datetime, timedelta

from dateutil import parser
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .forms import DateForm
from .models import Player, Team, Game, PlayerSeasonStats, TeamSeasonStats


# ==============================================================================
# Scores views
# ==============================================================================
def index(request):
    """Index page (with daily game scores).
    """
    return render_score_page(request, 'main/index.html', datetime.today(), 'Home')


def score(request, date: str):
    """Scores page.
    """
    date_obj = parser.parse(date)
    return render_score_page(request, 'main/score.html', date_obj, date)


@csrf_protect
def render_score_page(request, page: str, date: datetime.date, title: str):
    """Render generic score page.
    """
    games = Game.objects.filter(game_date=date.strftime("%b %d, %Y"))

    # Validate date input
    if request.method == 'POST':
        form = DateForm(request.POST)
        date_input = parser.parse(form.data.get('date'))
        if form.is_valid():
            return redirect('main:score', date=date_input)

    context = {
        'title': title,
        'today_display': date.strftime("%b %d, %Y"),
        'tomorrow': (date + timedelta(1)).strftime("%m-%d-%Y"),
        'tomorrow_display': (date + timedelta(1)).strftime("%b %d, %Y"),
        'yesterday': (date - timedelta(1)).strftime("%m-%d-%Y"),
        'yesterday_display': (date - timedelta(1)).strftime("%b %d, %Y"),
        'games': games
    }
    return render(request, page, context)


# ==============================================================================
# Players views
# ==============================================================================
def players(request, player_id: str):
    """Individual player stats page.
    """
    try:
        player = Player.objects.get(player_id=player_id)
        stats = PlayerSeasonStats.objects.filter(player__player_id=player_id)
    except Player.DoesNotExist:
        return redirect('main:player_list')

    context = {
        'title': player.get_full_name(),
        'player': player,
        'data': stats
    }
    return render(request, 'main/players.html', context)


def player_games(request, player_id: str, season: str):
    """Individual player season game log page.
    """
    try:
        player = Player.objects.get(player_id=player_id)
    except Player.DoesNotExist:
        return redirect('main:player_list')

    context = {
        'title': player.get_full_name(),
        'player': player
    }
    return render(request, 'main/player_games.html', context)


def player_list(request):
    """Player list page.
    """
    player_obj = Player.objects.all()
    ranked_players = []
    unranked_players = []
    for player in player_obj:
        if player.rank < 1:
            unranked_players.append(player)
        else:
            ranked_players.append(player)

    context = {
        'title': "Player List",
        'ranked_players': sorted(ranked_players, key=lambda p: p.rank),
        'unranked_players': unranked_players
    }
    return render(request, 'main/player_list.html', context)


# ==============================================================================
# Teams views
# ==============================================================================
def teams(request, team_id: str):
    """Individual team stats page.
    """
    try:
        team = Team.objects.get(team_id=team_id)
    except Team.DoesNotExist:
        return redirect('main:team_list')

    context = {
        'title': team.get_full_name(),
        'team': team,
    }
    return render(request, 'main/teams.html', context)


def team_games(request, team_id: str, season: str):
    """Individual team season game log page.
    """
    try:
        team = Team.objects.get(team_id=team_id)
        stats = TeamSeasonStats.objects.filter(team__team_id=team_id)
    except Team.DoesNotExist:
        return redirect('main:team_list')

    context = {
        'title': team.get_full_name(),
        'team': team,
        'data': stats
    }
    return render(request, 'main/team_games.html', context)


def team_list(request):
    """Team list page.
    """
    context = {
        'title': "Team List",
        'teams': Team.objects.all()
    }
    return render(request, 'main/team_list.html', context)


# ==============================================================================
# Games views
# ==============================================================================
def box_score(request, game_id: str):
    """Single game box score page.
    """
    try:
        game = Game.objects.get(game_id=game_id)
    except Game.DoesNotExist:
        return redirect('main:index')

    context = {
        'title': 'Boxscore',
        'game': game,
    }
    return render(request, 'main/boxscore.html', context)


# ==============================================================================
# Standing views
# ==============================================================================
def standing(request):
    """Season standing page.
    """
    context = {
        'title': 'Standing',
        'headers': [('bg-danger', 'East Conference'), ('bg-primary', 'West Conference')],
        'east_conf_standing': Team.get_east_standing(),
        'west_conf_standing': Team.get_west_standing()
    }
    return render(request, 'main/standing.html', context)
