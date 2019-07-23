# Generated by Django 2.2.3 on 2019-07-09 19:18

import pandas as pd
from django.db import migrations


def load_team_data(apps, schema_editor):
    Team = apps.get_model("main", "Team")

    print("Migrate Individual Team Data.")

    data = pd.read_json('../main/data/team_summary.json')  # type: pd.DataFrame

    for team in data.itertuples(index=False):
        Team(
            team_id=team.TEAM_ID,
            team_abb=team.TEAM_ABBREVIATION,
            team_conf=team.TEAM_CONFERENCE,
            team_div=team.TEAM_DIVISION,
            team_city=team.TEAM_CITY,
            team_name=team.TEAM_NAME,
            wins=team.W,
            losses=team.L,
            nba_debut=team.MIN_YEAR,
            max_year=team.MAX_YEAR
        ).save()


def undo(apps, schema_editor):
    Team = apps.get_model("main", "Team")
    Team.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_team_data, undo)
    ]
