"""Main App Views Module

@date: 06/02/2019
@author: Larry Shi
"""

from datetime import datetime, timedelta

from dateutil import parser
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from nba_py import Scoreboard
from simplejson.decoder import JSONDecoder

from . import PLAYER_PHOTO_LINK
from .forms import DateForm
from .models import Player, Team, Game


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
    """Render generic score page"""
    # Get data and store in dictionary
    daily_games = Scoreboard(day=date.day, month=date.month, year=date.year)
    games = {game_num: {} for game_num in daily_games.game_header()['GAME_SEQUENCE']}
    for _, data in daily_games.line_score().iterrows():
        if data['TEAM_ID'] in daily_games.game_header()['HOME_TEAM_ID'].values:
            prefix = 'HOME'
        else:
            prefix = 'AWAY'

        team_data = games[data['GAME_SEQUENCE']]
        team_data[f'{prefix}_TEAM'] = data['TEAM_ABBREVIATION']
        team_data[f'{prefix}_TEAM_WINS_LOSSES'] = data['TEAM_WINS_LOSSES']
        team_data[f'{prefix}_TEAM_LOGO'] = f"images/{data['TEAM_ABBREVIATION']}.png"
        team_data[f'{prefix}_TEAM_PTS'] = data['PTS']

    # Determine winner
    for game_num, game in games.items():
        if game['HOME_TEAM_PTS'] > game['AWAY_TEAM_PTS']:
            game['WINNER'] = game['HOME_TEAM']
        else:
            game['WINNER'] = game['AWAY_TEAM']

        # Determine game status and broadcaster
        game['STATUS'] = daily_games.game_header()['GAME_STATUS_TEXT'][game_num - 1]

        # Determine game broadcaster
        broadcaster = daily_games.game_header()['NATL_TV_BROADCASTER_ABBREVIATION'][game_num - 1]
        if not broadcaster:
            game['BROADCASTER'] = ""
        else:
            game['BROADCASTER'] = broadcaster

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
        player = Player.objects.filter(player_id=player_id)[0]
    except (IndexError, Player.DoesNotExist):
        return redirect(index)

    context = {
        'title': player.get_full_name(),
        'player': player,
        'player_photo': PLAYER_PHOTO_LINK.format(player_id=player_id),
        'team_logo': f"images/{player.team.team_abb}.png"
    }
    return render(request, 'main/players.html', context)


def player_list(request):
    """Player list page.
    """
    player_obj = Player.objects.all()
    ranked_players = []
    unranked_players = []
    for player in player_obj:
        if player.rank == 0:
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
        team = Team.objects.filter(team_id=team_id)[0]
    except (IndexError, Team.DoesNotExist):
        return redirect(index)

    context = {
        'title': team.get_full_name(),
        'team': team,
        'team_logo': f"images/{team.team_abb}.png"
    }
    return render(request, 'main/teams.html', context)


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
        game = Game.objects.filter(game_id=game_id)[0]
    except (IndexError, Game.DoesNotExist):
        return redirect(index)

    # Organizes data
    inst = JSONDecoder()
    dnp_players = {
        Player.objects.filter(player_id=player_id)[0]: reason.strip()
        for player_id, reason in inst.decode(game.dnp_players).items()
        if len(Player.objects.filter(player_id=player_id)) > 0
    }
    inactive_player = [
        Player.objects.filter(player_id=player_id)[0]
        for player_id in inst.decode(game.inactive_players)
        if len(Player.objects.filter(player_id=player_id)) > 0
    ]
    player_game_log = [
        game.playergamelog_set.filter(player__player_id=player_id)[0]
        for player_id in inst.decode(game.order)
        if len(game.playergamelog_set.filter(player__player_id=player_id)) > 0
    ]

    context = {
        'title': 'Boxscore',
        'inactive_player': inactive_player,
        'game': game,
        'dnp_players': dnp_players,
        'home_team_logo': f"images/{game.home_team.team_abb}.png",
        'away_team_logo': f"images/{game.away_team.team_abb}.png",
        'team_game_log': game.teamgamelog_set.all(),
        'player_game_log': player_game_log,
    }
    return render(request, 'main/boxscore.html', context)
