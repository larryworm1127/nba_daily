# Generated by Django 2.2.3 on 2019-07-06 16:19

import json
import time

from django.db import migrations
from nba_py import game


def load_data(apps, schema_editor):
    Game = apps.get_model('main', 'Game')
    Team = apps.get_model('main', 'Team')

    for game_obj in Game.objects.all():
        print(game_obj.game_id)
        boxscore_summary = game.BoxscoreSummary(game_obj.game_id)
        inact_player_data = boxscore_summary.inactive_players()
        inactive_players = [p_data['PLAYER_ID'] for _, p_data in inact_player_data.iterrows()]
        game_obj.inactive_players = json.dumps(inactive_players)

        home_team = Team.objects.filter(team_id=boxscore_summary.game_summary()['HOME_TEAM_ID'])[0]
        away_team = Team.objects.filter(team_id=boxscore_summary.game_summary()['VISITOR_TEAM_ID'])[0]
        game_obj.home_team = home_team
        game_obj.away_team = away_team

        game_obj.save()
        time.sleep(0.2)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0033_update_dnp_player_data'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]
