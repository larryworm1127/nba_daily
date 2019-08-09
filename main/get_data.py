"""Data Retrieval Module

This module calls API to retrieve data from 'stats.nba.com' and creates Django
model fixture using the data.

@date: 07/07/2019
@author: Larry Shi
"""
import logging
import sys
import time
from typing import Dict, Tuple

import pandas as pd
import simplejson as json
from dateutil import parser
from nba_py import game, team, player, league, Scoreboard
from nba_py.constants import Player_or_Team as Pt


class CollectData:
    """NBA Data Collection Class.

    === Attributes ===
    season:
        the season to collect the data from.
    logger:
        a simple logger to track the collection of data.
    """
    season: str
    logger: logging.Logger

    def __init__(self, season: str) -> None:
        """Initializer.
        """
        # Configure logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            fmt='%(asctime)s %(levelname)s %(message)s',
            datefmt='%Y/%m/%d %I:%M:%S'
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

        # Retrieve initial data
        self.season = season
        self.team_list = team.TeamList().info()[['TEAM_ID']][:30]
        self.player_list = player.PlayerList(season=season).info()[['PERSON_ID', 'ROSTERSTATUS']]

    def get_standing_data(self) -> pd.DataFrame:
        """Retrieve season standing data using API.
        """
        self.logger.info('Retrieving standing data')
        year = int(f'20{self.season.split("-")[1]}')
        data = pd.DataFrame()
        data = data.append(Scoreboard(month=6, day=1, year=year).east_conf_standings_by_day(), ignore_index=True)
        data = data.append(Scoreboard(month=6, day=1, year=year).west_conf_standings_by_day(), ignore_index=True)
        return data

    def get_team_summary(self) -> pd.DataFrame:
        """Retrieve individual team summary data using API.
        """
        team_summary = pd.DataFrame()
        for team_data in self.team_list.itertuples(index=False):
            self.logger.info(f'Retrieving team summary data for {team_data.TEAM_ID}')

            data = team.TeamSummary(team_data.TEAM_ID, season=self.season).info()
            team_summary = team_summary.append(data, ignore_index=True)
            time.sleep(1)

        return team_summary

    def get_player_summary(self) -> pd.DataFrame:
        """Retrieve individual player summary data using API.
        """
        player_summary = pd.DataFrame()
        for player_data in self.player_list.itertuples(index=False):
            self.logger.info(f'Retrieving player summary data for {player_data.PERSON_ID}')

            if player_data.ROSTERSTATUS == 0:
                continue

            data = player.PlayerSummary(player_data.PERSON_ID).info()
            player_summary = player_summary.append(data, ignore_index=True)
            time.sleep(0.5)

        return player_summary

    def get_player_game_log(self) -> pd.DataFrame:
        """Retrieve individual player game log data using API.
        """
        self.logger.info('Retrieving player game log data.')
        game_log = league.GameLog(season=self.season, player_or_team=Pt.Player).overall()
        return game_log.fillna(0, inplace=True).round(3)

    def get_team_season_stats(self) -> pd.DataFrame:
        """Retrieve individual team season stats using API.
        """
        self.logger.info('Retrieve team season stats data.')
        season_stats = league.TeamStats(season=self.season).overall().round(3)
        return season_stats

    def get_boxscore_data(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """Retrieve individual game boxscore data using API.
        """
        boxscore_data = {}
        for game_id in [f'002180{"%04d" % index}' for index in range(1, 1231)]:
            self.logger.info(f'Retrieving boxscore data for {game_id}')

            boxscore = game.Boxscore(game_id, season=self.season)
            boxscore_summary = game.BoxscoreSummary(game_id, season=self.season)

            boxscore_data[game_id] = {
                'player_data': boxscore.player_stats(),
                'game_summary': boxscore_summary.game_summary(),
                'inactive_players': boxscore_summary.inactive_players(),
                'line_score': boxscore_summary.line_score()
            }
            time.sleep(0.5)

        return boxscore_data

    def get_team_game_log(self) -> pd.DataFrame:
        """Retrieve individual team game log data using API.
        """
        game_log = pd.DataFrame()
        for _team in self.team_list.itertuples(index=False):
            self.logger.info(f'Retrieving team game log data for {_team.TEAM_ID}')

            data = team.TeamGameLogs(_team.TEAM_ID, season=self.season).info()
            game_log = game_log.append(data, ignore_index=True)
            time.sleep(0.5)

        return game_log

    def get_player_season_stats(self) -> Tuple[Dict[int, Dict], Dict[int, Dict]]:
        """Retrieve individual player season stats using API.
        """
        season_stats = {}
        career_stats = {}
        for player_data in self.player_list.itertuples(index=False):
            self.logger.info(f'Retrieving player season stats data for {player_data.PERSON_ID}')

            if player_data.ROSTERSTATUS == 0:
                continue

            data = player.PlayerCareer(player_data.PERSON_ID)
            season_stats[player_data.PERSON_ID] = {
                'Regular': data.regular_season_totals().round(3),
                'Post': data.post_season_totals().round(3),
            }
            career_stats[player_data.PERSON_ID] = {
                'Regular': data.regular_season_career_totals().round(3),
                'Post': data.post_season_career_totals().round(3)
            }
            time.sleep(0.5)

        return season_stats, career_stats


class FixtureGenerator:
    """Django Model Fixture Generator Class.

    This class contains methods that automatically generates initial data
    fixtures for Django models. Each method generates fixture for a single model.

    The generated fixture is in JSON format and stored under the `fixtures`
    directory with the name of its corresponding model.
    """
    standing_data: pd.DataFrame
    team_summary: pd.DataFrame
    player_summary: pd.DataFrame
    player_game_log: pd.DataFrame
    boxscore_data: Dict[str, Dict[str, pd.DataFrame]]
    team_game_log: pd.DataFrame
    team_season_stats: pd.DataFrame
    player_season_stats: Dict[int, Dict[str, pd.DataFrame]]
    player_career_stats: Dict[int, Dict[str, pd.DataFrame]]

    def __init__(self, season: str) -> None:
        """Initializer.
        """
        data_inst = CollectData(season)

        # Data Attributes
        self.standing_data = data_inst.get_standing_data()
        self.team_summary = data_inst.get_team_summary()
        self.player_summary = data_inst.get_player_summary()
        self.player_game_log = data_inst.get_player_game_log()
        self.boxscore_data = data_inst.get_boxscore_data()
        self.team_game_log = data_inst.get_team_game_log()
        self.team_season_stats = data_inst.get_team_season_stats()

        player_career = data_inst.get_player_season_stats()
        self.player_season_stats = player_career[0]
        self.player_career_stats = player_career[1]

    def create_standing_fixture(self) -> None:
        """Creates fixture for <Standing> model.
        """
        result = []
        for team_data in self.standing_data.itertuples():
            data_fixture = {
                "model": "main.standing",
                "pk": team_data.Index + 1,
                "fields": {
                    "team": team_data.TEAM_ID,
                    "wins": team_data.W,
                    "losses": team_data.L,
                    "home_record": team_data.HOME_RECORD,
                    "away_record": team_data.ROAD_RECORD,
                    "win_percent": team_data.W_PCT
                }
            }
            result.append(data_fixture)

        # Write data to file
        with open('fixtures/main_standing.json', 'w+') as f:
            json.dump(result, f)

    def create_team_fixture(self) -> None:
        """Creates fixture for <Team> model.
        """
        result = []
        for data in self.team_summary.itertuples(index=False):
            data_fixture = {
                "model": "main.team",
                "pk": int(data.TEAM_ID),
                "fields": {
                    "team_abb": data.TEAM_ABBREVIATION,
                    "team_conf": data.TEAM_CONFERENCE,
                    "team_div": data.TEAM_DIVISION,
                    "team_city": data.TEAM_CITY,
                    "team_name": data.TEAM_NAME,
                    "wins": int(data.W),
                    "losses": int(data.L),
                    "nba_debut": data.MIN_YEAR,
                    "max_year": data.MAX_YEAR
                }
            }
            result.append(data_fixture)

        # Create a dummy team for players who switched teams during the season
        result.append({
            "model": "main.team",
            "pk": 0,
            "fields": {
                "team_abb": "TOT",
                "team_conf": "None",
                "team_div": "None",
                "team_city": "None",
                "team_name": "None",
                "wins": 82,
                "losses": 0,
                "nba_debut": "1950",
                "max_year": "2019"
            }
        })

        # Write data to file
        with open('fixtures/main_team.json', 'w+') as f:
            json.dump(result, f)

    def create_player_fixture(self) -> None:
        """Creates fixture for <Player> model.
        """
        result = []
        for data in self.player_summary.itertuples(index=False):
            data_fixture = {
                "model": "main.player",
                "pk": int(data.PERSON_ID),
                "fields": {
                    "team": int(data.TEAM_ID),
                    "first_name": data.FIRST_NAME,
                    "last_name": data.LAST_NAME,
                    "birth_date": data.BIRTHDATE[:10],
                    "draft_year": data.DRAFT_YEAR,
                    "draft_round": data.DRAFT_ROUND,
                    "draft_number": data.DRAFT_NUMBER,
                    "position": data.POSITION,
                    "jersey": 0 if data.JERSEY == '' else int(data.JERSEY),
                    "height": data.HEIGHT,
                    "weight": int(data.WEIGHT),
                    "school": "N/A" if data.SCHOOL is None or data.SCHOOL == ' ' else data.SCHOOL,
                    "country": data.COUNTRY,
                    "season_exp": int(data.SEASON_EXP)
                }
            }
            result.append(data_fixture)

        # Write data to file
        with open('fixtures/main_player.json', 'w+') as f:
            json.dump(result, f)

    def create_player_game_log_fixture(self) -> None:
        """Creates fixture for <PlayerGameLog> model.
        """
        result = []
        for data in self.player_game_log.itertuples():
            data_fixture = {
                "model": "main.playergamelog",
                "pk": data.Index + 1,
                "fields": {
                    "game": data.GAME_ID,
                    "matchup": data.MATCHUP,
                    "minutes": data.MIN,
                    "points": data.PTS,
                    "offense_reb": data.OREB,
                    "defense_reb": data.DREB,
                    "rebounds": data.REB,
                    "assists": data.AST,
                    "steals": data.STL,
                    "blocks": data.BLK,
                    "turnovers": data.TOV,
                    "fouls": data.PF,
                    "fg_made": data.FGM,
                    "fg_attempt": data.FGA,
                    "fg_percent": data.FG_PCT,
                    "fg3_made": data.FG3M,
                    "fg3_attempt": data.FG3A,
                    "fg3_percent": data.FG3_PCT,
                    "ft_made": data.FTM,
                    "ft_attempt": data.FTA,
                    "ft_percent": data.FT_PCT,
                    "result": data.WL,
                    "player": data.PLAYER_ID,
                    "curr_team": data.TEAM_ID,
                    "order": self.get_player_order(data.PLAYER_ID, data.GAME_ID),
                    "plus_minus": data.PLUS_MINUS
                }
            }
            result.append(data_fixture)

        # Write data to file
        with open('fixtures/main_player_game_log.json', 'w+') as f:
            json.dump(result, f)

    def get_player_order(self, player_id: int, game_id: str) -> int:
        """Returns the order in which the player appears in boxscore table.
        """
        boxscore = self.boxscore_data[game_id]['player_data']
        player_team = boxscore[boxscore.PLAYER_ID == player_id].TEAM_ID[0]
        opp_count = len(boxscore[boxscore.TEAM_ID != player_team])

        index = 0
        for item in boxscore.itertuples():
            if item.PLAYER_ID == player_id:
                index = item.Index

        if index >= opp_count and boxscore.TEAM_ID[0] != player_team:
            index -= opp_count

        return index

    def create_player_season_stats_fixture(self) -> None:
        """Creates fixture for <PlayerSeasonStats> model.
        """
        result = []
        for index, player_id, data in enumerate(self.player_season_stats.items()):
            for season_type in ['Regular', 'Post']:
                data_fixture = {
                    "model": "main.playerseasonstats",
                    "pk": index + 1,
                    "fields": {
                        "minutes": data[season_type].MIN,
                        "points": data[season_type].PTS,
                        "offense_reb": data[season_type].OREB,
                        "defense_reb": data[season_type].DREB,
                        "rebounds": data[season_type].REB,
                        "assists": data[season_type].AST,
                        "steals": data[season_type].STL,
                        "blocks": data[season_type].BLK,
                        "turnovers": data[season_type].TOV,
                        "fouls": data[season_type].PF,
                        "fg_made": data[season_type].FGM,
                        "fg_attempt": data[season_type].FGA,
                        "fg_percent": data[season_type].FG_PCT,
                        "fg3_made": data[season_type].FG3M,
                        "fg3_attempt": data[season_type].FG3A,
                        "fg3_percent": data[season_type].FG3_PCT,
                        "ft_made": data[season_type].FTM,
                        "ft_attempt": data[season_type].FTA,
                        "ft_percent": data[season_type].FT_PCT,
                        "season": data[season_type].SEASON_ID,
                        "season_type": season_type,
                        "curr_team": data[season_type].TEAM_ID,
                        "player": data[season_type].PLAYER_ID,
                        "games_played": data[season_type].GP,
                        "games_started": data[season_type].GS
                    }
                }
                result.append(data_fixture)

        # Write data to file
        with open('fixtures/main_player_season_stats.json', 'w+') as f:
            json.dump(result, f)

    def create_player_career_stats_fixture(self) -> None:
        """Creates fixture for <PlayerCareerStats> model.
        """
        result = []
        for index, player_id, data in enumerate(self.player_career_stats.items()):
            for season_type in ['Regular', 'Post']:
                data_fixture = {
                    "model": "main.playercareerstats",
                    "pk": index + 1,
                    "fields": {
                        "minutes": data[season_type].MIN,
                        "points": data[season_type].PTS,
                        "offense_reb": data[season_type].OREB,
                        "defense_reb": data[season_type].DREB,
                        "rebounds": data[season_type].REB,
                        "assists": data[season_type].AST,
                        "steals": data[season_type].STL,
                        "blocks": data[season_type].BLK,
                        "turnovers": data[season_type].TOV,
                        "fouls": data[season_type].PF,
                        "fg_made": data[season_type].FGM,
                        "fg_attempt": data[season_type].FGA,
                        "fg_percent": data[season_type].FG_PCT,
                        "fg3_made": data[season_type].FG3M,
                        "fg3_attempt": data[season_type].FG3A,
                        "fg3_percent": data[season_type].FG3_PCT,
                        "ft_made": data[season_type].FTM,
                        "ft_attempt": data[season_type].FTA,
                        "ft_percent": data[season_type].FT_PCT,
                        "season_type": season_type,
                        "player": data[season_type].PLAYER_ID,
                        "games_played": data[season_type].GP,
                        "games_started": data[season_type].GS
                    }
                }
                result.append(data_fixture)

        # Write data to file
        with open('fixtures/main_player_career_stats.json', 'w+') as f:
            json.dump(result, f)

    def create_team_game_log_fixture(self) -> None:
        """Creates fixture for <TeamGameLog> model.
        """
        result = []
        for data in self.team_game_log.itertuples():
            line_score = self.boxscore_data[data.GAME_ID]['line_score']
            index = 0 if line_score.TEAM_ID[0] == data.TEAM_ID else 1
            data_fixture = {
                "model": "main.teamgamelog",
                "pk": data.Index + 1,
                "fields": {
                    "matchup": data.MATCHUP,
                    "minutes": data.MIN,
                    "points": data.PTS,
                    "offense_reb": data.OREB,
                    "defense_reb": data.DREB,
                    "rebounds": data.REB,
                    "assists": data.AST,
                    "steals": data.STL,
                    "blocks": data.BLK,
                    "turnovers": data.TOV,
                    "fouls": data.PF,
                    "fg_made": data.FGM,
                    "fg_attempt": data.FGA,
                    "fg_percent": data.FG_PCT,
                    "fg3_made": data.FG3M,
                    "fg3_attempt": data.FG3A,
                    "fg3_percent": data.FG3_PCT,
                    "ft_made": data.FTM,
                    "ft_attempt": data.FTA,
                    "ft_percent": data.FT_PCT,
                    "result": data.WL,
                    "game": data.GAME_ID,
                    "team": data.TEAM_ID,
                    "curr_wins": data.W,
                    "curr_losses": data.L,
                    "pts_q1": line_score.PTS_QTR1[index],
                    "pts_q2": line_score.PTS_QTR2[index],
                    "pts_q3": line_score.PTS_QTR3[index],
                    "pts_q4": line_score.PTS_QTR4[index],
                    "pts_ot1": line_score.PTS_OT1[index],
                    "pts_ot2": line_score.PTS_OT2[index],
                    "pts_ot3": line_score.PTS_OT3[index],
                    "pts_ot4": line_score.PTS_OT4[index]
                }
            }
            result.append(data_fixture)

        # Write data to file
        with open('fixtures/main_team_game_log.json', 'w+') as f:
            json.dump(result, f)

    def create_team_season_stats_fixture(self) -> None:
        """Creates fixture for <TeamSeasonStats> model.
        """
        result = []
        for data in self.team_season_stats.itertuples():
            data_fixture = {
                "model": "main.teamseasonstats",
                "pk": data.Index + 1,
                "fields": {
                    "minutes": data.MIN,
                    "points": data.PTS,
                    "offense_reb": data.OREB,
                    "defense_reb": data.DREB,
                    "rebounds": data.REB,
                    "assists": data.AST,
                    "steals": data.STL,
                    "blocks": data.BLK,
                    "turnovers": data.TOV,
                    "fouls": data.PF,
                    "fg_made": data.FGM,
                    "fg_attempt": data.FGA,
                    "fg_percent": data.FG_PCT,
                    "fg3_made": data.FG3M,
                    "fg3_attempt": data.FG3A,
                    "fg3_percent": data.FG3_PCT,
                    "ft_made": data.FTM,
                    "ft_attempt": data.FTA,
                    "ft_percent": data.FT_PCT,
                    "season": "2018-19",
                    "team": data.TEAM_ID,
                    "wins": data.W,
                    "losses": data.L,
                    "win_percent": data.W_PCT
                }
            }
            result.append(data_fixture)

        # Write data to file
        with open('fixtures/main_team_season_stats.json', 'w+') as f:
            json.dump(result, f)

    def create_game_fixture(self) -> None:
        """Creates fixture for <Game> model.
        """
        result = []
        for game_id, data in self.boxscore_data.items():
            # Extract data from API responses
            broadcaster = data['game_summary'].NATL_TV_BROADCASTER_ABBREVIATION[0]
            inactive_players = [int(data.PLAYER_ID) for data in data['inactive_players'].itertuples()]
            dnp_players = {data.PLAYER_ID: data.COMMENT.strip() for data in data['player_data'].itertuples()
                           if len(data.COMMENT) != 0}

            # Create fixture
            data_fixture = {
                "model": "main.game",
                "pk": game_id,
                "fields": {
                    "season": "2018-19",
                    "game_date": parser.parse(data['game_summary'].GAME_DATE_EST[0]).strftime("%b %d, %Y"),
                    "dnp_players": json.dumps(dnp_players),
                    "inactive_players": json.dumps(inactive_players),
                    "home_team": int(data['game_summary'].HOME_TEAM_ID[0]),
                    "away_team": int(data['game_summary'].VISITOR_TEAM_ID[0]),
                    "broadcaster": broadcaster if broadcaster is not None else ''
                }
            }
            result.append(data_fixture)

        # Write data to file
        with open('fixtures/main_game.json', 'w+') as f:
            json.dump(result, f)


if __name__ == '__main__':
    inst = FixtureGenerator('2018-19')

    inst.create_standing_fixture()
    inst.create_team_fixture()
    inst.create_player_fixture()
    inst.create_player_game_log_fixture()
    inst.create_team_game_log_fixture()
    inst.create_player_season_stats_fixture()
    inst.create_player_career_stats_fixture()
    inst.create_team_season_stats_fixture()
    inst.create_game_fixture()
