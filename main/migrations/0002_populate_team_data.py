# Generated by Django 2.2.3 on 2019-07-09 19:18

from django.db import migrations
from simplejson import load


def load_team_data(apps, schema_editor):
    Team = apps.get_model("main", "Team")

    print("Migrate Individual Team Data.")

    with open('main/data/team_list.json') as f:
        teams = load(f)

    for team_id in teams['TEAM_ID'].values():
        with open(f'main/data/team_summary/2018-19/{team_id}.json') as f:
            data = load(f)

        Team(
            team_id=data['TEAM_ID']['0'],
            team_abb=data['TEAM_ABBREVIATION']['0'],
            team_conf=data['TEAM_CONFERENCE']['0'],
            team_div=data['TEAM_DIVISION']['0'],
            team_city=data['TEAM_CITY']['0'],
            team_name=data['TEAM_NAME']['0'],
            wins=data['W']['0'],
            losses=data['L']['0'],
            conf_rank=data['CONF_RANK']['0'],
            div_rank=data['DIV_RANK']['0'],
            season=data['SEASON_YEAR']['0'],
            nba_debut=data['MIN_YEAR']['0']
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
