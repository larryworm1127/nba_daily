from datetime import datetime
from django.shortcuts import render, redirect

from .models import Player
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
        'title': "Player",
        'summary_info': player_summary_info,
        'team_info': team_info,
        'player_photo': PLAYER_PHOTO_LINK.format(player_id=player_id),
        'team_logo': f"images/{team_info['TEAM_ABB']}.png"
    }
    return render(request, 'main/players.html', context)
