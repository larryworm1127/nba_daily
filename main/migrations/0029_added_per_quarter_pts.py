# Generated by Django 2.2.3 on 2019-07-06 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0028_add_start_dnp_player_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamgamelog',
            name='quarter1_pts',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamgamelog',
            name='quarter2_pts',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamgamelog',
            name='quarter3_pts',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamgamelog',
            name='quarter4_pts',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]