"""Main App Models Module

@date: 06/02/2019
@author: Larry Shi
"""
from datetime import datetime

from django.db import models


# ===================================================
# Team Data Models
# ===================================================
class Team(models.Model):
    """Individual team model.
    """
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
        """Return human-readable representation of the object.
        """
        return self.get_full_name()

    def get_full_name(self) -> str:
        """Return full name of the team: <team_city> <team_name>.
        """
        return f"{self.team_city} {self.team_name}"


# ===================================================
# Player Data Models
#
# methods:
#   - player.PlayerSummary(player_id)
# ===================================================
class Player(models.Model):
    """Individual player model.
    """
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
        """Return human-readable representation of the object.
        """
        return self.get_full_name()

    def get_full_name(self) -> str:
        """Return full name of the player: <first_name> <last_name>.
        """
        return f"{self.first_name} {self.last_name}"

    def get_age(self) -> int:
        """Return the calculated age of the player.
        """
        return datetime.today().year - datetime.strptime(self.birth_date, "%Y-%m-%d").year


# ===================================================
# Game Data Models
#
# methods:
#   - player.PlayerGameLog(player_id)
#   - team.TeamGameLog(team_id)
# ===================================================
class Game(models.Model):
    """Individual game model.
    """
    game_id = models.CharField(max_length=10)
    dnp_players = models.TextField(null=True, blank=True)
    inactive_players = models.TextField(null=True, blank=True)
    order = models.TextField(null=True, blank=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away')

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return f"{self.home_team} vs. {self.away_team}"


class GameLog(models.Model):
    """Game log template model.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
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
    """Individual player game log model.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    plus_minus = models.IntegerField()

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return f"{self.player.first_name} {self.player.last_name}, {self.matchup}"


class TeamGameLog(GameLog):
    """Individual team game log model.
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    curr_wins = models.IntegerField()
    curr_losses = models.IntegerField()
    pts_q1 = models.IntegerField()
    pts_q2 = models.IntegerField()
    pts_q3 = models.IntegerField()
    pts_q4 = models.IntegerField()
    pts_ot1 = models.IntegerField()
    pts_ot2 = models.IntegerField()
    pts_ot3 = models.IntegerField()
    pts_ot4 = models.IntegerField()

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return f"{self.team.team_city} {self.team.team_name}, {self.matchup}"
