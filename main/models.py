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
class Game(models.Model):
    game_id = models.CharField(max_length=10)


class GameLog(models.Model):
    game = models.ManyToManyField(Game)
    game_date = models.CharField(max_length=30)
    matchup = models.CharField(max_length=11)
    minutes = models.IntegerField()
    points = models.IntegerField()
    offense_reb = models.IntegerField()
    defense_reb = models.IntegerField()
    rebounds = models.IntegerField()
    assists = models.IntegerField()
    steals = models.IntegerField()
    blocks = models.IntegerField()
    turnovers = models.IntegerField()
    fouls = models.IntegerField()
    plus_minus = models.IntegerField()
    fg_made = models.IntegerField()
    fg_attempt = models.IntegerField()
    fg_percent = models.FloatField()
    fg3_made = models.IntegerField()
    fg3_attempt = models.IntegerField()
    fg3_percent = models.FloatField()
    ft_made = models.IntegerField()
    ft_attempt = models.IntegerField()
    ft_percent = models.FloatField()
    result = models.CharField(max_length=1)

    class Meta:
        abstract = True


class PlayerGameLog(GameLog):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.player.first_name} {self.player.last_name} {self.matchup}"


class TeamGameLog(GameLog):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    curr_wins = models.IntegerField()
    curr_losses = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.team.team_city} {self.team.team_name} {self.matchup}"
