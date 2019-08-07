"""Main App Models Module

@date: 06/02/2019
@author: Larry Shi
"""
from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse
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
    team_id = models.IntegerField(primary_key=True)
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

    def get_absolute_url(self):
        """Returns the url to access a particular player instance.
        """
        return reverse('main:teams', args=[self.team_id])


class Standing(models.Model):
    """Individual team standing model.
    """
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='standing')
    wins = models.IntegerField()
    losses = models.IntegerField()
    home_record = models.CharField(max_length=5)
    away_record = models.CharField(max_length=5)
    win_percent = models.FloatField()

    class Meta:
        """Standing Property Meta Class.
        """
        ordering = ['-win_percent', '-wins', '-home_record', '-away_record']

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return f'{self.team.get_full_name()} {self.get_wins_losses()}'

    @property
    def seed(self) -> int:
        """Return the seed of current team.
        """
        conf_teams = Standing.objects.filter(team__team_conf=self.team.team_conf)
        return list(conf_teams).index(self) + 1

    def get_wins_losses(self) -> str:
        """Return display wins and losses string.
        """
        return f'{self.wins}-{self.losses}'


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
    player_id = models.IntegerField(primary_key=True)
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

    class Meta:
        """Player Property Meta Class.
        """
        ordering = ['last_name', 'first_name']

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

    def get_latest_stats(self) -> PlayerSeasonStats:
        """Return the latest player season stats object.

        TODO: change the season to something more dynamic
        """
        try:
            return self.season_stats.get(
                season_type='Regular',
                season='2018-19'
            )
        except PlayerSeasonStats.MultipleObjectsReturned:
            return self.season_stats.get(
                season_type='Regular',
                season='2018-19',
                curr_team__team_id=0
            )

    def get_absolute_url(self):
        """Returns the url to access a particular player instance.
        """
        return reverse('main:players', args=[self.player_id])


# ==============================================================================
# Season Stats Models
# ==============================================================================
class SeasonStats(models.Model):
    """Season stats template model.
    """
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
    fg_percent = models.FloatField(validators=[MaxValueValidator(1)])
    fg3_made = models.FloatField()
    fg3_attempt = models.FloatField()
    fg3_percent = models.FloatField(validators=[MaxValueValidator(1)])
    ft_made = models.FloatField()
    ft_attempt = models.FloatField()
    ft_percent = models.FloatField(validators=[MaxValueValidator(1)])

    class Meta:
        abstract = True


class TeamSeasonStats(SeasonStats):
    """Individual team season stats model.
    """
    season = models.CharField(max_length=10)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='season_stats')
    wins = models.IntegerField()
    losses = models.IntegerField()
    win_percent = models.FloatField()

    class Meta:
        """TeamSeasonStats Property Meta Class.
        """
        db_table = 'main_team_season_stats'

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return self.team.get_full_name()


class PlayerCareerStats(SeasonStats):
    """Individual player career total stats model.
    """
    SEASON_TYPE = [
        ('REG', 'Regular'),
        ('POST', 'Post')
    ]

    class Meta:
        """PlayerCareerStats Property Meta Class.
        """
        db_table = 'main_player_career_stats'

    season_type = models.CharField(max_length=7, choices=SEASON_TYPE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='career_stats')
    games_played = models.IntegerField()
    games_started = models.IntegerField()

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return self.player.get_full_name()


class PlayerSeasonStats(SeasonStats):
    """Individual player season total stats model.
    """
    SEASON_TYPE = [
        ('REG', 'Regular'),
        ('POST', 'POST')
    ]

    class Meta:
        """PlayerSeasonStats Property Meta Class.
        """
        db_table = 'main_player_season_stats'
        ordering = ['-season']

    season = models.CharField(max_length=10)
    season_type = models.CharField(max_length=7, choices=SEASON_TYPE)
    curr_team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='season_stats')
    games_played = models.IntegerField(validators=[MaxValueValidator(82)])
    games_started = models.IntegerField(validators=[MaxValueValidator(82)])

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
    game_id = models.CharField(max_length=10, primary_key=True)
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
            Player.objects.get(pk=player_id)
            for player_id in inst.decode(self.inactive_players)
            if Player.objects.filter(pk=player_id).count() > 0
        ]

        return inactive_player

    def home_team_game_log(self) -> TeamGameLog:
        """Return the home team game log object.
        """
        return self.team_game_log.get(team=self.home_team)

    def away_team_game_log(self) -> TeamGameLog:
        """Return the away team game log object.
        """
        return self.team_game_log.get(team=self.away_team)

    def overtime(self) -> int:
        """Return the number of overtimes played in the game.
        """
        home_game_log = self.home_team_game_log()
        away_game_log = self.away_team_game_log()

        if home_game_log.pts_ot4 > 0 or away_game_log.pts_ot4 > 0:
            return 4
        elif home_game_log.pts_ot3 > 0 or away_game_log.pts_ot3 > 0:
            return 3
        elif home_game_log.pts_ot2 > 0 or away_game_log.pts_ot2 > 0:
            return 2
        elif home_game_log.pts_ot1 > 0 or away_game_log.pts_ot1 > 0:
            return 1

        return 0

    def get_absolute_url(self) -> str:
        """Returns the url to access a particular player instance.
        """
        return reverse('main:boxscore', args=[self.game_id])

    def get_score_page_url(self) -> str:
        """Returns the url to scores page of a particular date.
        """
        return reverse('main:score', args=[self.game_date])

    @staticmethod
    def get_closest_game_date(curr_date: datetime.date) -> datetime.date:
        """Return the closest date with games.

        === Attributes ===
        curr_date:
            the current date to search from.
        """
        game_dates = [datetime.strptime(game.game_date, "%b %d, %Y").date()
                      for game in Game.objects.all().iterator()]
        return min(game_dates, key=lambda date: abs(date - curr_date))


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
    fg_percent = models.FloatField(validators=[MaxValueValidator(1)])
    fg3_made = models.IntegerField()
    fg3_attempt = models.IntegerField()
    fg3_percent = models.FloatField(validators=[MaxValueValidator(1)])
    ft_made = models.IntegerField()
    ft_attempt = models.IntegerField()
    ft_percent = models.FloatField(validators=[MaxValueValidator(1)])
    result = models.CharField(max_length=1)

    class Meta:
        abstract = True


class TeamGameLog(GameLog):
    """Individual team game log model.
    """
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='team_game_log')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_game_log')
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

    class Meta:
        """TeamGameLog Property Meta Class.
        """
        db_table = 'main_team_game_log'
        ordering = ['-game']

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return f"{self.team.team_city} {self.team.team_name}, {self.matchup}"

    def get_plus_minus(self) -> int:
        """Return the plus-minus of the team in that game.
        """
        opp_team = self.game.away_team if self.game.home_team == self.team else self.game.home_team
        opp_score = self.game.team_game_log.get(team=opp_team).points
        return self.points - opp_score

    def get_player_game_logs(self) -> List[PlayerGameLog]:
        """Return a list of player game log object in order of display.
        """
        num_players = self.player_game_log.all().count()
        return [self.player_game_log.get(order=index) for index in range(num_players)
                if self.player_game_log.filter(order=index).count() > 0]


class PlayerGameLog(GameLog):
    """Individual player game log model.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='game_log')
    team_game_log = models.ForeignKey(TeamGameLog, on_delete=models.CASCADE, related_name='player_game_log')
    order = models.IntegerField()
    plus_minus = models.IntegerField()

    class Meta:
        """PlayerGameLog Property Meta Class.
        """
        db_table = 'main_player_game_log'
        ordering = ['-game']

    def __str__(self) -> str:
        """Return human-readable representation of the object.
        """
        return f"{self.player.first_name} {self.player.last_name}, {self.matchup}"
