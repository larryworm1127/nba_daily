"""

@date: 07/07/2019
@author: Larry Shi
"""
import logging
import os
import sys
import time

import pandas as pd
from nba_py import game, team, player, league
from nba_py.constants import Player_or_Team
from simplejson import load, dump


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
        self.season = season

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

    def get_team_list(self) -> None:
        """Retrieve team list data using API.
        """
        self.logger.info(f'Retrieving team list data')

        team_list = team.TeamList().info()[['TEAM_ID']]
        team_list.to_json('data/team_list.json')

    def get_player_list(self) -> None:
        """Retrieve player list data using API.

        === Attributes ===
        season:
            the season to get the player list from.
        """
        self.logger.info('Retrieving player list data')

        player_list = player.PlayerList(season=self.season).info()[['PERSON_ID', 'ROSTERSTATUS']]
        player_list.to_json(f'data/{self.season}/player_list.json')

    def get_player_league_leader(self) -> None:
        """Retrieve player league leader data using API.

        === Attributes ===
        season:
            the season to get the league leader data from.
        """
        self.logger.info('Retrieve league leader data')

        leaders = league.Leaders(stat_category="EFF", season=self.season).results()[['PLAYER_ID', 'RANK']]
        leaders.to_json(f'data/{self.season}/player_leaders.json')

    def get_team_summary(self) -> None:
        """Retrieve individual team summary data using API.

        === Attributes ===
        season:
            the season to get the team summary from.
        """
        teams = pd.read_json('data/team_list.json')  # type: pd.DataFrame

        # Collect data and add them to the main data frame
        team_summ = pd.DataFrame()
        for team_data in teams.itertuples(index=False):
            self.logger.info(f'Retrieving team summary data for {team_data.TEAM_ID}')

            data = team.TeamSummary(team_data.TEAM_ID, season=self.season).info()  # type: pd.DataFrame
            team_summ = team_summ.append(data, ignore_index=True)

            time.sleep(0.5)

        # Remove data columns that won't be needed
        team_summ = team_summ.drop(columns=[
            'SEASON_YEAR',
            'TEAM_CODE',
            'PCT',
            'CONF_RANK',
            'DIV_RANK'
        ])
        team_summ.to_json('data/team_summary.json')

    def get_player_summary(self) -> None:
        """Retrieve individual player summary data using API.
        """
        players = pd.read_json(f'data/{self.season}/player_list.json')  # type: pd.DataFrame

        # Collect data and add them to the main data frame
        player_summ = pd.DataFrame()
        for player_data in players.itertuples(index=False):
            self.logger.info(f'Retrieving player summary data for {player_data.PERSON_ID}')

            if player_data.ROSTERSTATUS == 0:
                continue

            data = player.PlayerSummary(player_data.PERSON_ID).info()  # type: pd.DataFrame
            player_summ = player_summ.append(data, ignore_index=True)

            time.sleep(0.5)

        # Remove data columns that won't be needed
        player_summ = player_summ.drop(columns=[
            'DISPLAY_FIRST_LAST',
            'DISPLAY_LAST_COMMA_FIRST',
            'DISPLAY_FI_LAST',
            'LAST_AFFILIATION',
            'TEAM_CODE',
            'PLAYERCODE',
            'DLEAGUE_FLAG',
            'NBA_FLAG',
            'GAMES_PLAYED_FLAG',
            'TEAM_ABBREVIATION',
            'TEAM_NAME',
            'TEAM_CITY'
        ])
        player_summ.to_json(f'data/{self.season}/player_summary.json')

    def get_player_game_log(self) -> None:
        """Retrieve individual player game log data using API.

        === Attributes ===
        season:
            the season to get the player game log from.
        """
        self.logger.info('Retrieving player game log data.')

        data = league.GameLog(season=self.season, player_or_team=Player_or_Team.Player).overall()  # type: pd.DataFrame
        data.fillna(0, inplace=True)
        data = data.drop(columns=[
            'VIDEO_AVAILABLE',
            'TEAM_ABBREVIATION',
            'TEAM_NAME',
            'SEASON_ID',
            'PLAYER_NAME'
        ])
        data.to_json(f'data/{self.season}/player_game_log.json')

    def get_player_season_stats(self) -> None:
        """Retrieve individual player season stats using API.

        === Attributes ===
        season:
            the season to get the player stats from.
        """
        players = pd.read_json(f'data/{self.season}/player_list.json')  # type: pd.DataFrame

        reg_season = pd.DataFrame()
        reg_season_total = pd.DataFrame()
        post_season = pd.DataFrame()
        post_season_total = pd.DataFrame()
        for player_data in players.itertuples(index=False):
            self.logger.info(f'Retrieving player season stats data for {player_data.PERSON_ID}')

            if player_data.ROSTERSTATUS == 0:
                continue

            data = player.PlayerCareer(player_data.PERSON_ID)
            reg_season = reg_season.append(data.regular_season_totals().drop(columns=[
                'LEAGUE_ID',
                'PLAYER_AGE'
            ]), ignore_index=True)

            reg_season_total = reg_season_total.append(data.regular_season_career_totals().drop(columns=[
                'LEAGUE_ID',
            ]), ignore_index=True)

            post_season = post_season.append(data.post_season_totals().drop(columns=[
                'TEAM_ABBREVIATION',
                'LEAGUE_ID',
                'PLAYER_AGE'
            ]), ignore_index=True)

            post_season_total = post_season_total.append(data.post_season_career_totals().drop(columns=[
                'LEAGUE_ID'
            ]), ignore_index=True)

            time.sleep(0.5)

        reg_season.to_json('data/player_regular_season_stats.json')
        reg_season_total.to_json('data/player_regular_season_total.json')
        post_season.to_json('data/player_post_season_stats.json')
        post_season_total.to_json('data/player_post_season_total.json')

    def get_team_game_log(self) -> None:
        """Retrieve individual team game log data using API.

        === Attributes ===
        season:
            the season to get the team game log from.
        """
        with open('data/team_list.json') as f:
            teams = load(f)['TEAM_ID'].values()

        all_game_log = pd.DataFrame()
        for team_id in teams:
            self.logger.info(f'Retrieving team game log data for {team_id}')

            data = team.TeamGameLogs(team_id, season=self.season).info()  # type: pd.DataFrame
            all_game_log = all_game_log.append(data, ignore_index=True)

            time.sleep(0.5)

        all_game_log.to_json(f'data/{self.season}/team_game_log.json')

    def get_team_season_stats(self) -> None:
        """Retrieve individual team season stats using API.

        === Attributes ===
        season:
            the season to get the team stats from.
        """
        self.logger.info('Retrieve team season stats data.')

        data = league.TeamStats(season=self.season).overall()
        data = data.drop(columns=[
            'CFID',
            'CFPARAMS',
            'TEAM_NAME',
        ])
        data.to_json(f'data/{self.season}/team_stats.json')

    def get_game_list(self) -> None:
        """Retrieve game list data from team game log.

        === Attributes ===
        season:
            the season in which the games are played.
        """
        self.logger.info('Retrieving game list data')

        game_log = league.GameLog(season=self.season,
                                  player_or_team=Player_or_Team.Team).overall()  # type: pd.DataFrame
        games = {data.GAME_ID for data in game_log.itertuples(index=False)}

        with open(f'data/{self.season}/game_list.json', 'w+') as f:
            dump(list(games), f)

    def get_box_score(self) -> None:
        """Retrieve individual game player box score data using API.

        === Attributes ===
        season:
            the season in which the games are played.
        """
        with open(f'data/{self.season}/game_list.json') as f:
            games = load(f)

        for game_id in games:
            self.logger.info(f'Retrieving box score data for {game_id}')

            data = game.Boxscore(game_id, season=self.season).player_stats()
            data.to_json(f'data/{self.season}/boxscore/{game_id}.json')

            # time.sleep(0.5)

        assert len(os.listdir(f'data/{self.season}/boxscore')) == 1230

    def get_box_score_summary(self) -> None:
        """Retrieve individual game box score summary data using API.

        === Attributes ===
        season:
            the season in which the games are played.
        """
        with open(f'data/{self.season}/game_list.json') as f:
            games = load(f)

        for game_id in games:
            self.logger.info(f'Retrieving box score summary data for {game_id}')

            data = game.BoxscoreSummary(game_id, season=self.season)
            game_summary = data.game_summary().drop(columns=[
                'GAME_SEQUENCE',
                'SEASON',
                'LIVE_PERIOD_TIME_BCAST',
                'LIVE_PC_TIME',
                'LIVE_PERIOD',
                'WH_STATUS',
                'GAME_STATUS_ID',
                'GAME_STATUS_TEXT',
                'GAMECODE'
            ]).to_json()

            line_score = data.line_score().drop(columns=[
                'GAME_DATE_EST',
                'GAME_SEQUENCE',
                'TEAM_ABBREVIATION',
                'TEAM_CITY_NAME',
                'TEAM_NICKNAME',
                'PTS',
            ]).to_json()

            inactive_player = data.inactive_players().drop(columns=[
                'FIRST_NAME',
                'LAST_NAME',
                'JERSEY_NUM',
                'TEAM_ID',
                'TEAM_CITY',
                'TEAM_NAME',
                'TEAM_ABBREVIATION'
            ]).to_json()

            with open(f'data/{self.season}/boxscore_summary/{game_id}.json', 'w+') as f:
                result = {
                    'GAME_SUMMARY': game_summary,
                    'LINE_SCORE': line_score,
                    'INACTIVE_PLAYER': inactive_player
                }
                dump(result, f)

            time.sleep(0.5)

        assert len(os.listdir(f'data/{self.season}/boxscore_summary')) == 1230


if __name__ == '__main__':
    inst = CollectData('2018-19')

    # inst.get_team_list()
    # inst.get_player_list()
    # inst.get_player_league_leader()

    # inst.get_team_summary()
    # inst.get_player_summary()

    # inst.get_player_game_log()
    # inst.get_team_game_log()
    # inst.get_player_season_stats()
    # inst.get_team_season_stats()

    inst.get_game_list()
    inst.get_box_score()
    inst.get_box_score_summary()
