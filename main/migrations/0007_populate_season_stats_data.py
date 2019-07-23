# Generated by Django 2.2.3 on 2019-07-23 17:38

import pandas as pd
from django.db import migrations


def load_team_data(apps, schema_editor):
    Team = apps.get_model('main', 'Team')
    TeamSeasonStats = apps.get_model('main', 'TeamSeasonStats')

    print("Migrate Individual Team Season Stats Data.")

    data = pd.read_json('../main/data/2018-19/team_stats.json')  # type: pd.DataFrame
    for team_data in data.itertuples(index=False):

        TeamSeasonStats(
            team=Team.objects.get(team_id=team_data.TEAM_ID),
            minutes=team_data.MIN,
            points=team_data.PTS,
            offense_reb=team_data.OREB,
            defense_reb=team_data.DREB,
            rebounds=team_data.REB,
            assists=team_data.AST,
            steals=team_data.STL,
            blocks=team_data.BLK,
            turnovers=team_data.TOV,
            fouls=team_data.PF,
            fg_made=team_data.FGM,
            fg_attempt=team_data.FGA,
            fg_percent=team_data.FG_PCT,
            fg3_made=team_data.FG3M,
            fg3_attempt=team_data.FG3A,
            fg3_percent=team_data.FG3_PCT,
            ft_made=team_data.FTM,
            ft_attempt=team_data.FTA,
            ft_percent=team_data.FT_PCT,
            plus_minus=team_data.PLUS_MINUS
        ).save()


def load_player_data(apps, schema_editor):
    Player = apps.get_model('main', 'Player')
    PlayerSeasonStats = apps.get_model('main', 'PlayerSeasonStats')

    print("Migrate Individual Player Season Stats Data.")

    data = pd.read_json('../main/data/2018-19/player_stats.json')  # type: pd.DataFrame
    for player_data in data.itertuples(index=False):
        try:
            player_obj = Player.objects.get(player_id=player_data.PLAYER_ID)
        except Player.DoesNotExist:
            continue

        PlayerSeasonStats(
            player=player_obj,
            games_played=player_data.GP,
            minutes=player_data.MIN,
            points=player_data.PTS,
            offense_reb=player_data.OREB,
            defense_reb=player_data.DREB,
            rebounds=player_data.REB,
            assists=player_data.AST,
            steals=player_data.STL,
            blocks=player_data.BLK,
            turnovers=player_data.TOV,
            fouls=player_data.PF,
            fg_made=player_data.FGM,
            fg_attempt=player_data.FGA,
            fg_percent=player_data.FG_PCT,
            fg3_made=player_data.FG3M,
            fg3_attempt=player_data.FG3A,
            fg3_percent=player_data.FG3_PCT,
            ft_made=player_data.FTM,
            ft_attempt=player_data.FTA,
            ft_percent=player_data.FT_PCT,
            plus_minus=player_data.PLUS_MINUS,
            double_double=player_data.DD2,
            triple_double=player_data.TD3
        ).save()


def undo(apps, schema_editor):
    TeamSeasonStats = apps.get_model('main', 'TeamSeasonStats')
    TeamSeasonStats.objects.all().delete()

    PlayerSeasonStats = apps.get_model('main', 'PlayerSeasonStats')
    PlayerSeasonStats.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_populate_player_game_log_data'),
    ]

    operations = [
        migrations.RunPython(load_team_data, undo),
        migrations.RunPython(load_player_data, undo)
    ]
