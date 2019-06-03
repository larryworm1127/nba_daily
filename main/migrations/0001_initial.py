# Generated by Django 2.2.1 on 2019-06-03 00:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                ('draft_year', models.CharField(max_length=10)),
                ('draft_round', models.CharField(max_length=10)),
                ('draft_number', models.CharField(max_length=10)),
                ('position', models.CharField(max_length=10)),
                ('jersey', models.IntegerField()),
                ('height', models.CharField(max_length=5)),
                ('weight', models.IntegerField()),
                ('school', models.CharField(max_length=35)),
                ('country', models.CharField(max_length=20)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Team')),
            ],
        ),
    ]
