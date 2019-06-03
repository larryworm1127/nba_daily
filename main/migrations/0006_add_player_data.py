# Generated by Django 2.2.1 on 2019-06-03 01:55

import time
from django.db import migrations
from nba_py import player


def load_player_data(apps, schema_editor):
    Player = apps.get_model("main", "Player")

    file = open('a.txt', 'w+')

    players_df = player.PlayerList().info()
    for player_id in players_df['PERSON_ID'].values:
        data = player.PlayerSummary(player_id=player_id).info()
        file.write(str(data) + '\n')
        Team = apps.get_model("main", "Team").objects.filter(team_id=data['TEAM_ID'].values[0])
        if len(Team) > 0:
            Player(
                team=Team[0],
                first_name=data['FIRST_NAME'].values[0],
                last_name=data['LAST_NAME'].values[0],
                birth_date=data['BIRTHDATE'].values[0][:10],
                player_id=data['PERSON_ID'].values[0],
                draft_year=data['DRAFT_YEAR'].values[0],
                draft_round=data['DRAFT_ROUND'].values[0],
                draft_number=data['DRAFT_NUMBER'].values[0],
                position=data['POSITION'].values[0],
                jersey=0 if data['JERSEY'].values[-1] == '' else int(data['JERSEY'].values[-1]),
                height=data['HEIGHT'].values[0],
                weight=int(data['WEIGHT'].values[0]),
                school=data['SCHOOL'].values[0],
                country=data['COUNTRY'].values[0]
            ).save()

        time.sleep(1)
    file.close()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_player'),
    ]

    operations = [
        migrations.RunPython(load_player_data)
    ]
