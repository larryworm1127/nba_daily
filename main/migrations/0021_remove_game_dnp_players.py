# Generated by Django 2.2.3 on 2019-07-01 23:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0020_add_dnp_player_field'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='dnp_players',
        ),
    ]