# Generated by Django 2.2.2 on 2019-06-30 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_populate_emtpy_school_cells'),
    ]

    operations = [
        migrations.CreateModel(
            name='TeamGameLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_date', models.CharField(max_length=30)),
                ('matchup', models.CharField(max_length=11)),
                ('minutes', models.IntegerField()),
                ('points', models.IntegerField()),
                ('offense_reb', models.IntegerField()),
                ('defense_reb', models.IntegerField()),
                ('rebounds', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('steals', models.IntegerField()),
                ('blocks', models.IntegerField()),
                ('turnovers', models.IntegerField()),
                ('fouls', models.IntegerField()),
                ('fg_made', models.IntegerField()),
                ('fg_attempt', models.IntegerField()),
                ('fg_percent', models.FloatField()),
                ('fg3_made', models.IntegerField()),
                ('fg3_attempt', models.IntegerField()),
                ('fg3_percent', models.FloatField()),
                ('ft_made', models.IntegerField()),
                ('ft_attempt', models.IntegerField()),
                ('ft_percent', models.FloatField()),
                ('result', models.CharField(max_length=1)),
                ('curr_wins', models.IntegerField()),
                ('curr_losses', models.IntegerField()),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerGameLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_date', models.CharField(max_length=30)),
                ('matchup', models.CharField(max_length=11)),
                ('minutes', models.IntegerField()),
                ('points', models.IntegerField()),
                ('offense_reb', models.IntegerField()),
                ('defense_reb', models.IntegerField()),
                ('rebounds', models.IntegerField()),
                ('assists', models.IntegerField()),
                ('steals', models.IntegerField()),
                ('blocks', models.IntegerField()),
                ('turnovers', models.IntegerField()),
                ('fouls', models.IntegerField()),
                ('fg_made', models.IntegerField()),
                ('fg_attempt', models.IntegerField()),
                ('fg_percent', models.FloatField()),
                ('fg3_made', models.IntegerField()),
                ('fg3_attempt', models.IntegerField()),
                ('fg3_percent', models.FloatField()),
                ('ft_made', models.IntegerField()),
                ('ft_attempt', models.IntegerField()),
                ('ft_percent', models.FloatField()),
                ('result', models.CharField(max_length=1)),
                ('plus_minus', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.CharField(max_length=10)),
                ('dnp_players', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Player')),
                ('player_stats', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.PlayerGameLog')),
                ('team_stats', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.TeamGameLog')),
            ],
        ),
    ]