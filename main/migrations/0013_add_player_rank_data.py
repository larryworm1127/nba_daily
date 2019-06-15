# Generated by Django 2.2.1 on 2019-06-12 01:35

import time
from django.db import migrations
from nba_py import league


def load_player_data(apps, schema_editor):
    Player = apps.get_model("main", "Player")

    data = league.Leaders(stat_category="EFF").results()
    for rank, player_data in data.iterrows():
        player_obj = Player.objects.filter(player_id=player_data["PLAYER_ID"])
        if len(player_obj) > 0:
            player_obj[0].rank = rank + 1
            player_obj[0].save()

        time.sleep(1)  # pause for 1 sec to prevent too many requests


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_player_rank'),
    ]

    operations = [
        migrations.RunPython(load_player_data)
    ]