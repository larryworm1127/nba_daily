"""Main App Models Module

@date: 06/02/2019
@author: Larry Shi
"""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from django.db import models
from simplejson.decoder import JSONDecoder

from . import PLAYER_PHOTO_LINK


# ==============================================================================
# Team Data Models
#
# methods:
#   - team.TeamSummary(team_id).info()
# ==============================================================================
class Team(models.Model):
    """Individual team model.
    """
    team_id = models.IntegerField()
    team_abb = models.CharField(max_length=3)
    team_conf = models.CharField(max_length=4)
    team_div = models.CharField(max_length=10)
    team_city = models.CharField(max_length=15)
    team_name = models.CharField(max_length=15)
    wins = models.IntegerField()
    losses = models.IntegerField()
    nba_debut = models.CharField(max_length=4)
    max_year = models.CharField(max_length=4)

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return self.get_full_name()

    def get_full_name(self) -> str:
        """Return full name of the team: <team_city> <team_name>.
        """
        return f"{self.team_city} {self.team_name}"

    def get_logo_path(self) -> str:
        """Return the team logo path.
        """
        return f"images/{self.team_abb}.png"

    @staticmethod
    def get_east_standing() -> List[Team]:
        """Return the East conference teams in standing order.
        """
        result = [team for team in Team.objects.all() if team.team_conf == 'East']
        return sorted(result, key=lambda t: t.conf_rank)

    @staticmethod
    def get_west_standing() -> List[Team]:
        """Return the West conference teams in standing order.
        """
        result = [team for team in Team.objects.all() if team.team_conf == 'West']
        return sorted(result, key=lambda t: t.conf_rank)


class TeamStanding(models.Model):
    """Individual team standing model.
    """
    team = models.OneToOneField(Team, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()
    home_wins = models.IntegerField()
    home_losses = models.IntegerField()
    away_wins = models.IntegerField()
    away_losses = models.IntegerField()


# ==============================================================================
# Player Data Models
#
# methods:
#   - player.PlayerSummary(player_id).info()
# ==============================================================================
class Player(models.Model):
    """Individual player model.
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    birth_date = models.CharField(max_length=20)
    player_id = models.IntegerField()
    draft_year = models.CharField(max_length=20)
    draft_round = models.CharField(max_length=20)
    draft_number = models.CharField(max_length=20)
    position = models.CharField(max_length=20)
    jersey = models.IntegerField()
    height = models.CharField(max_length=5)
    weight = models.IntegerField()
    school = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    season_exp = models.IntegerField()
    rank = models.IntegerField()

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

    def get_photo_url(self) -> str:
        """Return the URL to player photo.
        """
        return str(PLAYER_PHOTO_LINK.render(player_id=self.player_id))


# ==============================================================================
# Season Stats Models
# ==============================================================================
class SeasonStats(models.Model):
    """Season stats template model.
    """
    season = models.CharField(max_length=10)
    minutes = models.FloatField()
    points = models.FloatField()
    offense_reb = models.FloatField()
    defense_reb = models.FloatField()
    rebounds = models.FloatField()
    assists = models.FloatField()
    steals = models.FloatField()
    blocks = models.FloatField()
    turnovers = models.FloatField()
    fouls = models.FloatField()
    fg_made = models.FloatField()
    fg_attempt = models.FloatField()
    fg_percent = models.FloatField()
    fg3_made = models.FloatField()
    fg3_attempt = models.FloatField()
    fg3_percent = models.FloatField()
    ft_made = models.FloatField()
    ft_attempt = models.FloatField()
    ft_percent = models.FloatField()
    plus_minus = models.FloatField()

    class Meta:
        abstract = True


class TeamSeasonStats(SeasonStats):
    """Individual team season stats model.
    """
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    wins = models.IntegerField()
    losses = models.IntegerField()
    win_percent = models.FloatField()

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return self.team.get_full_name()


class PlayerSeasonStats(SeasonStats):
    """Individual player season stats model.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    curr_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    games_played = models.IntegerField()
    double_double = models.IntegerField()
    triple_double = models.IntegerField()

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return self.player.get_full_name()


# ==============================================================================
# Game Data Models
#
# methods:
#   - game.Boxscore(game_id).player_stats()
#   - game.BoxscoreSummary(game_id).inactive_players()
#   - game.BoxscoreSummary(game_id).game_summary()
# ==============================================================================
class Game(models.Model):
    """Individual game model.
    """
    game_id = models.CharField(max_length=10)
    season = models.CharField(max_length=7)
    game_date = models.CharField(max_length=30)
    dnp_players = models.TextField(blank=True)
    inactive_players = models.TextField(blank=True)
    home_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home')
    away_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away')
    broadcaster = models.CharField(max_length=10, blank=True)

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return f"{self.home_team} vs. {self.away_team}"

    def get_dnp_players(self) -> Dict[Player, str]:
        """Return formatted DNP player data.
        """
        inst = JSONDecoder()
        dnp_players = {
            Player.objects.get(player_id=player_id): reason
            for player_id, reason in inst.decode(self.dnp_players).items()
            if Player.objects.filter(player_id=player_id).count() > 0
        }

        return dnp_players

    def get_inactive_players(self) -> List[Player]:
        """Return formatted inactive player data.
        """
        inst = JSONDecoder()
        inactive_player = [
            Player.objects.get(player_id=player_id)
            for player_id in inst.decode(self.inactive_players)
            if Player.objects.filter(player_id=player_id).count() > 0
        ]

        return inactive_player

    def home_team_game_log(self) -> TeamGameLog:
        """Return the home team game log object.
        """
        return self.teamgamelog_set.get(team=self.home_team)

    def away_team_game_log(self) -> TeamGameLog:
        """Return the away team game log object.
        """
        return self.teamgamelog_set.get(team=self.away_team)


# ==============================================================================
# Game Log Data Models
#
# methods:
#   - player.PlayerGameLog(player_id).info()
#   - team.TeamGameLog(team_id).info()
#   - game.Boxscore(game_id).player_stats()
# ==============================================================================
class GameLog(models.Model):
    """Game log template model.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
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
    pts_ot1 = models.IntegerField(default=0)
    pts_ot2 = models.IntegerField(default=0)
    pts_ot3 = models.IntegerField(default=0)
    pts_ot4 = models.IntegerField(default=0)

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return f"{self.team.team_city} {self.team.team_name}, {self.matchup}"

    def get_plus_minus(self) -> int:
        """Return the plus-minus of the team in that game.
        """
        opp_team = self.game.away_team if self.game.home_team == self.team else self.game.home_team
        opp_score = self.game.teamgamelog_set.get(team=opp_team).points
        return self.points - opp_score

    def get_player_game_logs(self) -> List[PlayerGameLog]:
        """Return a list of player game log object in order of display.
        """
        num_players = self.playergamelog_set.all().count()
        return [self.playergamelog_set.get(order=index) for index in range(num_players)
                if self.playergamelog_set.filter(order=index).count() > 0]


class PlayerGameLog(GameLog):
    """Individual player game log model.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team_game_log = models.ForeignKey(TeamGameLog, on_delete=models.CASCADE)
    order = models.IntegerField()
    plus_minus = models.IntegerField()

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return f"{self.player.first_name} {self.player.last_name}, {self.matchup}"
