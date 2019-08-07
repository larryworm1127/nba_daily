# Generated by Django 2.2.3 on 2019-07-10 14:01

import pandas as pd
from django.db import migrations
from simplejson import load


def load_data(apps, schema_editor):
    TeamGameLog = apps.get_model('main', 'TeamGameLog')
    Team = apps.get_model('main', 'Team')
    Game = apps.get_model('main', 'Game')

    print("Migrate Individual Team Game Log Data.")

    game_log = pd.read_json(f'main/data/2018-19/team_game_log.json', dtype={'Game_ID': str})  # type: pd.DataFrame
    for team_data in game_log.itertuples(index=False):
        team_obj = Team.objects.get(team_id=team_data.Team_ID)

        with open(f'main/data/2018-19/boxscore/{team_data.Game_ID}.json') as f:
            boxscore_summary = load(f)

        line_score = pd.read_json(boxscore_summary['LINE_SCORE'])
        index = 0 if line_score.TEAM_ID[0] == team_obj.team_id else 1
        TeamGameLog(
            team=team_obj,
            game=Game.objects.get(game_id=team_data.Game_ID),
            curr_wins=team_data.W,
            curr_losses=team_data.L,
            matchup=team_data.MATCHUP,
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
            result=team_data.WL,
            pts_q1=line_score['PTS_QTR1'][index],
            pts_q2=line_score['PTS_QTR2'][index],
            pts_q3=line_score['PTS_QTR3'][index],
            pts_q4=line_score['PTS_QTR4'][index],
            pts_ot1=line_score['PTS_OT1'][index],
            pts_ot2=line_score['PTS_OT2'][index],
            pts_ot3=line_score['PTS_OT3'][index],
            pts_ot4=line_score['PTS_OT4'][index]
        ).save()


def undo(apps, schema_editor):
    TeamGameLog = apps.get_model("main", "TeamGameLog")
    TeamGameLog.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_populate_game_data'),
    ]

    operations = [
        migrations.RunPython(load_data, undo)
    ]