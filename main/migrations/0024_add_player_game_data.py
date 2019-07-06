# Generated by Django 2.2.3 on 2019-07-04 01:59

import time

from django.db import migrations
from nba_py import player


def load_data(apps, schema_editor):
    PlayerGameLog = apps.get_model('main', 'PlayerGameLog')
    Game = apps.get_model('main', 'Game')
    Players = apps.get_model('main', 'Player')
    for player_obj in Players.objects.all():
        data = player.PlayerGameLogs(player_obj.player_id, season='2018-19').info()
        print(f"{player_obj.first_name} {player_obj.last_name}")

        for _, player_data in data.iterrows():
            game = Game.objects.filter(game_id=player_data['Game_ID'])[0]
            PlayerGameLog(
                game=game,
                player=player_obj,
                plus_minus=player_data['PLUS_MINUS'],
                game_date=player_data['GAME_DATE'],
                matchup=player_data['MATCHUP'],
                minutes=player_data['MIN'],
                points=player_data['PTS'],
                offense_reb=player_data['OREB'],
                defense_reb=player_data['DREB'],
                rebounds=player_data['REB'],
                assists=player_data['AST'],
                steals=player_data['STL'],
                blocks=player_data['BLK'],
                turnovers=player_data['TOV'],
                fouls=player_data['PF'],
                fg_made=player_data['FGM'],
                fg_attempt=player_data['FGA'],
                fg_percent=player_data['FG_PCT'],
                fg3_made=player_data['FG3M'],
                fg3_attempt=player_data['FG3A'],
                fg3_percent=player_data['FG3_PCT'],
                ft_made=player_data['FTM'],
                ft_attempt=player_data['FTA'],
                ft_percent=player_data['FT_PCT'],
                result=player_data['WL']
            ).save()

        time.sleep(0.5)


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_add_team_gamelog_data'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]