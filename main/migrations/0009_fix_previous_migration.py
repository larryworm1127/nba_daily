# Generated by Django 2.2.1 on 2019-06-09 20:05

import time
from django.db import migrations
from nba_py import player


def load_player_data(apps, schema_editor):
    Player = apps.get_model("main", "Player")

    players_df = player.PlayerList().info()
    for player_id in players_df['PERSON_ID'].values:
        player_obj = Player.objects.filter(player_id=player_id)
        if len(player_obj) > 0:
            player_obj[0].season_exp = player.PlayerSummary(player_id=player_id).info()['SEASON_EXP'].values[0]
            player_obj[0].save()

        time.sleep(1)  # pause for 1 sec to prevent too many requests


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_add_player_season_exp'),
    ]

    operations = [
        migrations.RunPython(load_player_data)
    ]