# Generated by Django 2.2.3 on 2019-07-10 13:27

import math
from dateutil import parser
from django.db import migrations
from pandas import read_json
from simplejson import load, dumps


def load_game_data(apps, schema_editor):
    Game = apps.get_model('main', 'Game')
    Team = apps.get_model('main', 'Team')

    print("Migrate Individual Game Data.")

    for game_id in [f'002180{"%04d" % index}' for index in range(1, 1231)]:
        with open(f'main/data/2018-19/boxscore/{game_id}.json') as f:
            boxscore_summary = load(f)

        boxscore = read_json(boxscore_summary['PLAYER_DATA'])
        game_summary = read_json(boxscore_summary['GAME_SUMMARY'])
        inactive_data = read_json(boxscore_summary['INACTIVE_PLAYER'])

        dnp_players = {
            data['PLAYER_ID']: data['COMMENT'].strip() for _, data in boxscore.iterrows() if math.isnan(data['PF'])
        }
        inactive_players = [
            int(p_data['PLAYER_ID']) for _, p_data in inactive_data.iterrows()
        ]
        broadcaster = game_summary['NATL_TV_BROADCASTER_ABBREVIATION'][0]
        Game(
            game_id=game_id,
            season='2018-19',
            game_date=parser.parse(game_summary['GAME_DATE_EST'][0]).strftime("%b %d, %Y"),
            broadcaster=broadcaster if not isinstance(broadcaster, float) else '',
            dnp_players=dumps(dnp_players),
            inactive_players=dumps(inactive_players),
            home_team=Team.objects.get(team_id=game_summary['HOME_TEAM_ID']),
            away_team=Team.objects.get(team_id=game_summary['VISITOR_TEAM_ID'])
        ).save()


def undo(apps, schema_editor):
    Game = apps.get_model("main", "Game")
    Game.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_populate_player_data'),
    ]

    operations = [
        migrations.RunPython(load_game_data, undo)
    ]