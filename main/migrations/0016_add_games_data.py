# Generated by Django 2.2.2 on 2019-06-30 17:24

import time

from django.db import migrations
from nba_py import team


def load_data(apps, schema_editor):
    TeamGameLog = apps.get_model('main', 'TeamGameLog')
    Teams = apps.get_model('main', 'Team')
    for team_obj in Teams.objects.all():
        data = team.TeamGameLogs(team_obj.team_id).info()

        for _, team_data in data.iterrows():
            TeamGameLog(
                team=team_obj,
                curr_wins=team_data['W'],
                curr_losses=team_data['L'],
                game_date=team_data['GAME_DATE'],
                matchup=team_data['MATCHUP'],
                minutes=team_data['MIN'],
                points=team_data['PTS'],
                offense_reb=team_data['OREB'],
                defense_reb=team_data['DREB'],
                rebounds=team_data['REB'],
                assists=team_data['AST'],
                steals=team_data['STL'],
                blocks=team_data['BLK'],
                turnovers=team_data['TOV'],
                fouls=team_data['PF'],
                fg_made=team_data['FGM'],
                fg_attempt=team_data['FGA'],
                fg_percent=team_data['FG_PCT'],
                fg3_made=team_data['FG3M'],
                fg3_attempt=team_data['FG3A'],
                fg3_percent=team_data['FG3_PCT'],
                ft_made=team_data['FTM'],
                ft_attempt=team_data['FTA'],
                ft_percent=team_data['FT_PCT'],
                result=team_data['WL']
            ).save()

        time.sleep(0.5)


class Migration(migrations.Migration):
    dependencies = [
        ('main', '0015_playergamelog_teamgamelog'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]