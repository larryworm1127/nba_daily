"""Main App Models Module

@date: 06/02/2019
@author: Larry Shi
"""

from django.db import models


# ===================================================
# Team Data Models
# ===================================================
class Team(models.Model):
    team_id = models.IntegerField()
    team_abb = models.CharField(max_length=3)
    team_conf = models.CharField(max_length=4)
    team_div = models.CharField(max_length=10)
    team_city = models.CharField(max_length=15)
    team_name = models.CharField(max_length=15)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    conf_rank = models.IntegerField(default=0)
    div_rank = models.IntegerField(default=0)
    season_year = models.CharField(max_length=7, default='2018-19')
    nba_debut = models.CharField(max_length=4, default=4)

    def __str__(self) -> str:
        return f"{self.team_city} {self.team_name}"


# ===================================================
# Player Data Models
#
# methods:
#   - player.PlayerSummary(player_id)
# ===================================================
class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birth_date = models.CharField(max_length=20)
    player_id = models.IntegerField()
    draft_year = models.CharField(max_length=10)
    draft_round = models.CharField(max_length=10)
    draft_number = models.CharField(max_length=10)
    position = models.CharField(max_length=10)
    jersey = models.IntegerField()
    height = models.CharField(max_length=5)
    weight = models.IntegerField()
    school = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    season_exp = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


# ===================================================
# Game Data Models
# ===================================================

