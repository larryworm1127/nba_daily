from datetime import datetime
from django.shortcuts import render, redirect

from .models import Player, Team
from . import PLAYER_PHOTO_LINK


def index(request):
    """Index page.
    """
    context = {
        'title': "Home"
    }
    return render(request, 'main/index.html', context)


def players(request, player_id):
    """Individual player stats page.
    """
    try:
        player = Player.objects.filter(player_id=player_id)[0]
        player_summary_info = {
            "NAME": f"{player.first_name} {player.last_name}",
            "JERSEY": player.jersey,
            "POSITION": player.position,
            "HEIGHT": player.height,
            "WEIGHT": player.weight,
            "SCHOOL": player.school if player.school is not None else "N/A",
            "COUNTRY": player.country,
            "DRAFT_YEAR": player.draft_year,
            "DRAFT_ROUND": player.draft_round,
            "DRAFT_NUMBER": player.draft_number,
            "SEASON_EXP": player.season_exp,
            "BIRTH_DATE": player.birth_date,
            "AGE": datetime.today().year - datetime.strptime(player.birth_date, "%Y-%m-%d").year
        }

        team_info = {
            "TEAM_ABB": player.team.team_abb,
            "TEAM_CITY": player.team.team_city,
            "TEAM_NAME": player.team.team_name,
            "TEAM_ID": player.team.team_id
        }
    except (IndexError, Player.DoesNotExist):
        return redirect(index)

    context = {
        'title': player_summary_info["NAME"],
        'summary_info': player_summary_info,
        'team_info': team_info,
        'player_photo': PLAYER_PHOTO_LINK.format(player_id=player_id),
        'team_logo': f"images/{team_info['TEAM_ABB']}.png"
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


def teams(request, team_id):
    """Individual team stats page.
    """
    try:
        team = Team.objects.filter(team_id=team_id)[0]
        team_summary_info = {
            "NAME": f"{team.team_city} {team.team_name}",
            "TEAM_ABB": team.team_abb,
            "TEAM_CONF": team.team_conf,
            "TEAM_DIV": team.team_div,
            "CONF_RANK": team.conf_rank,
            "DIV_RANK": team.div_rank,
            "NBA_DEBUT": team.nba_debut,
            "WINS": team.wins,
            "LOSSES": team.losses,
            "SEASON_YEAR": team.season_year
        }
    except (IndexError, Team.DoesNotExist):
        return redirect(index)

    context = {
        'title': team_summary_info["NAME"],
        'summary_info': team_summary_info,
        'team_logo': f"images/{team_summary_info['TEAM_ABB']}.png"
    }
    return render(request, 'main/teams.html', context)
