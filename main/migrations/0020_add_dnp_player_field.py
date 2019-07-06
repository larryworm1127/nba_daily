# Generated by Django 2.2.3 on 2019-07-01 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_update_games_relationship'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='dnp_players',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Player'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='playergamelog',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Game'),
        ),
        migrations.AlterField(
            model_name='teamgamelog',
            name='game',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Game'),
        ),
    ]