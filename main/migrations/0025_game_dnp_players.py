# Generated by Django 2.2.3 on 2019-07-04 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0024_add_player_game_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='dnp_players',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Player'),
        ),
    ]