# Generated by Django 2.2.3 on 2019-07-06 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_update_dnp_players_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='starters',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='game',
            name='dnp_players',
        ),
        migrations.AddField(
            model_name='game',
            name='dnp_players',
            field=models.TextField(blank=True, null=True),
        ),
    ]