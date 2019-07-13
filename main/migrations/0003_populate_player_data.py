# Generated by Django 2.2.3 on 2019-07-10 02:17

import math
from django.db import migrations
from pandas import read_json
from simplejson import load


def load_player_data(apps, schema_editor):
    Player = apps.get_model("main", "Player")

    print("Migrate Individual Player Data.")

    with open('main/data/player_list.json') as f:
        players = load(f)

    with open('main/data/player_leaders.json') as f:
        leaders = load(f)

    for player_id in players['PERSON_ID'].values():
        try:
            data = read_json(f'main/data/player_summary/{player_id}.json')
        except ValueError:
            continue

        try:
            player_rank = list(leaders['PLAYER_ID'].values()).index(player_id) + 1
        except ValueError:
            player_rank = -1

        try:
            school = "N/A" if math.isnan(data['SCHOOL'][0]) else data['SCHOOL'][0]
        except TypeError:
            school = "N/A" if data['SCHOOL'][0] == ' ' else data['SCHOOL'][0]

        Player(
            team=apps.get_model("main", "Team").objects.filter(team_id=data['TEAM_ID'][0])[0],
            first_name=data['FIRST_NAME'][0],
            last_name=data['LAST_NAME'][0],
            birth_date=data['BIRTHDATE'][0][:10],
            player_id=data['PERSON_ID'][0],
            draft_year=data['DRAFT_YEAR'][0],
            draft_round=data['DRAFT_ROUND'][0],
            draft_number=data['DRAFT_NUMBER'][0],
            position=data['POSITION'][0],
            jersey=0 if data['JERSEY'][0] == '' else int(data['JERSEY'][0]),
            height=data['HEIGHT'][0],
            weight=int(data['WEIGHT'][0]),
            school=school,
            country=data['COUNTRY'][0],
            season_exp=data['SEASON_EXP'][0],
            rank=player_rank
        ).save()


def undo(apps, schema_editor):
    Player = apps.get_model("main", "Player")
    Player.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_populate_team_data'),
    ]

    operations = [
        migrations.RunPython(load_player_data, undo)
    ]
