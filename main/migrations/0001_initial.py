# Generated by Django 2.2.3 on 2019-08-04 00:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.CharField(max_length=10)),
                ('season', models.CharField(max_length=7)),
                ('game_date', models.CharField(max_length=30)),
                ('dnp_players', models.TextField(blank=True)),
                ('inactive_players', models.TextField(blank=True)),
                ('broadcaster', models.CharField(blank=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('birth_date', models.CharField(max_length=20)),
                ('player_id', models.IntegerField()),
                ('draft_year', models.CharField(max_length=20)),
                ('draft_round', models.CharField(max_length=20)),
                ('draft_number', models.CharField(max_length=20)),
                ('position', models.CharField(max_length=20)),
                ('jersey', models.IntegerField()),
                ('height', models.CharField(max_length=5)),
                ('weight', models.IntegerField()),
                ('school', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('season_exp', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.IntegerField()),
                ('team_abb', models.CharField(max_length=3)),
                ('team_conf', models.CharField(max_length=4)),
                ('team_div', models.CharField(max_length=10)),
                ('team_city', models.CharField(max_length=15)),
                ('team_name', models.CharField(max_length=15)),
                ('wins', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('nba_debut', models.CharField(max_length=4)),
                ('max_year', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Standing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wins', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('home_record', models.CharField(max_length=5)),
                ('away_record', models.CharField(max_length=5)),
                ('win_percent', models.FloatField()),
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='standing', to='main.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamSeasonStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minutes', models.FloatField()),
                ('points', models.FloatField()),
                ('offense_reb', models.FloatField()),
                ('defense_reb', models.FloatField()),
                ('rebounds', models.FloatField()),
                ('assists', models.FloatField()),
                ('steals', models.FloatField()),
                ('blocks', models.FloatField()),
                ('turnovers', models.FloatField()),
                ('fouls', models.FloatField()),
                ('fg_made', models.FloatField()),
                ('fg_attempt', models.FloatField()),
                ('fg_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('fg3_made', models.FloatField()),
                ('fg3_attempt', models.FloatField()),
                ('fg3_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('ft_made', models.FloatField()),
                ('ft_attempt', models.FloatField()),
                ('ft_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('season', models.CharField(max_length=10)),
                ('wins', models.IntegerField()),
                ('losses', models.IntegerField()),
                ('win_percent', models.FloatField()),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_stats', to='main.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TeamGameLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('fg_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('fg3_made', models.IntegerField()),
                ('fg3_attempt', models.IntegerField()),
                ('fg3_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('ft_made', models.IntegerField()),
                ('ft_attempt', models.IntegerField()),
                ('ft_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('result', models.CharField(max_length=1)),
                ('curr_wins', models.IntegerField()),
                ('curr_losses', models.IntegerField()),
                ('pts_q1', models.IntegerField()),
                ('pts_q2', models.IntegerField()),
                ('pts_q3', models.IntegerField()),
                ('pts_q4', models.IntegerField()),
                ('pts_ot1', models.IntegerField(default=0)),
                ('pts_ot2', models.IntegerField(default=0)),
                ('pts_ot3', models.IntegerField(default=0)),
                ('pts_ot4', models.IntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_game_log', to='main.Game')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_game_log', to='main.Team')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerTotalStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minutes', models.FloatField()),
                ('points', models.FloatField()),
                ('offense_reb', models.FloatField()),
                ('defense_reb', models.FloatField()),
                ('rebounds', models.FloatField()),
                ('assists', models.FloatField()),
                ('steals', models.FloatField()),
                ('blocks', models.FloatField()),
                ('turnovers', models.FloatField()),
                ('fouls', models.FloatField()),
                ('fg_made', models.FloatField()),
                ('fg_attempt', models.FloatField()),
                ('fg_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('fg3_made', models.FloatField()),
                ('fg3_attempt', models.FloatField()),
                ('fg3_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('ft_made', models.FloatField()),
                ('ft_attempt', models.FloatField()),
                ('ft_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('season_type', models.CharField(choices=[('REG', 'Regular'), ('POST', 'Post')], max_length=7)),
                ('games_played', models.IntegerField()),
                ('games_started', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='career_stats', to='main.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerSeasonStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minutes', models.FloatField()),
                ('points', models.FloatField()),
                ('offense_reb', models.FloatField()),
                ('defense_reb', models.FloatField()),
                ('rebounds', models.FloatField()),
                ('assists', models.FloatField()),
                ('steals', models.FloatField()),
                ('blocks', models.FloatField()),
                ('turnovers', models.FloatField()),
                ('fouls', models.FloatField()),
                ('fg_made', models.FloatField()),
                ('fg_attempt', models.FloatField()),
                ('fg_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('fg3_made', models.FloatField()),
                ('fg3_attempt', models.FloatField()),
                ('fg3_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('ft_made', models.FloatField()),
                ('ft_attempt', models.FloatField()),
                ('ft_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('season', models.CharField(max_length=10)),
                ('season_type', models.CharField(choices=[('REG', 'Regular'), ('POST', 'POST')], max_length=7)),
                ('games_played', models.IntegerField(validators=[django.core.validators.MaxValueValidator(82)])),
                ('games_started', models.IntegerField(validators=[django.core.validators.MaxValueValidator(82)])),
                ('curr_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Team')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_stats', to='main.Player')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlayerGameLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('fg_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('fg3_made', models.IntegerField()),
                ('fg3_attempt', models.IntegerField()),
                ('fg3_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('ft_made', models.IntegerField()),
                ('ft_attempt', models.IntegerField()),
                ('ft_percent', models.FloatField(validators=[django.core.validators.MaxValueValidator(1)])),
                ('result', models.CharField(max_length=1)),
                ('order', models.IntegerField()),
                ('plus_minus', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_log', to='main.Player')),
                ('team_game_log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_game_log', to='main.TeamGameLog')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='player',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='away_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away', to='main.Team'),
        ),
        migrations.AddField(
            model_name='game',
            name='home_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home', to='main.Team'),
        ),
    ]
