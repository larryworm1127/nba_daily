# Generated by Django 2.2.1 on 2019-06-12 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_add_team_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='rank',
            field=models.IntegerField(default=0),
        ),
    ]