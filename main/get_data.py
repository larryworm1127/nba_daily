"""

@date: 07/07/2019
@author: Larry Shi
"""
import logging
import sys
import time

import pandas as pd
import simplejson as json
from dateutil import parser
from nba_py import game, team, player, league, Scoreboard
from nba_py.constants import Player_or_Team


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

        team_list = team.TeamList().info()[['TEAM_ID']][:30]
        team_list.to_json('data/team_list.json')

    def get_player_list(self) -> None:
        """Retrieve player list data using API.
        """
        self.logger.info('Retrieving player list data')

        player_list = player.PlayerList(season=self.season).info()[['PERSON_ID', 'ROSTERSTATUS']]
        player_list.to_json(f'data/{self.season}/player_list.json')

    def get_standing_data(self) -> None:
        """Retrieve season standing data using API.
        """
        self.logger.info('Retrieving standing data')

        year = f'20{self.season.split("-")[1]}'
        data = pd.DataFrame()
        data = data.append(Scoreboard(month=6, day=1, year=int(year)).east_conf_standings_by_day(), ignore_index=True)
        data = data.append(Scoreboard(month=6, day=1, year=int(year)).west_conf_standings_by_day(), ignore_index=True)

        data = data.drop(columns=[
            'TEAM',
            'LEAGUE_ID',
            'SEASON_ID',
            'STANDINGSDATE',
            'CONFERENCE',
            'G'
        ])
        data.to_json(f'data/{self.season}/standing.json')

    def get_player_league_leader(self) -> None:
        """Retrieve player league leader data using API.
        """
        self.logger.info('Retrieve league leader data')

        leaders = league.Leaders(stat_category="EFF", season=self.season).results()[['PLAYER_ID', 'RANK']]
        leaders.to_json(f'data/{self.season}/player_leaders.json')

    def get_team_summary(self) -> None:
        """Retrieve individual team summary data using API.
        """
        teams = pd.read_json('data/team_list.json')  # type: pd.DataFrame

        # Collect data and add them to the main data frame
        result = []
        for team_data in teams.itertuples(index=False):
            self.logger.info(f'Retrieving team summary data for {team_data.TEAM_ID}')

            data = team.TeamSummary(team_data.TEAM_ID, season=self.season).info()  # type: pd.DataFrame
            data_fixture = {
                "model": "main.team",
                "pk": int(data.TEAM_ID[0]),
                "fields": {
                    "team_abb": data.TEAM_ABBREVIATION[0],
                    "team_conf": data.TEAM_CONFERENCE[0],
                    "team_div": data.TEAM_DIVISION[0],
                    "team_city": data.TEAM_CITY[0],
                    "team_name": data.TEAM_NAME[0],
                    "wins": int(data.W[0]),
                    "losses": int(data.L[0]),
                    "nba_debut": data.MIN_YEAR[0],
                    "max_year": data.MAX_YEAR[0]
                }
            }
            result.append(data_fixture)
            time.sleep(0.5)

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
                "max_year": "2018-19"
            }
        })

        # Write data to file
        print(result)
        with open('fixtures/main_team.json', 'w+') as f:
            json.dump(result, f)

    def get_player_summary(self) -> None:
        """Retrieve individual player summary data using API.
        """
        players = pd.read_json(f'data/{self.season}/player_list.json')  # type: pd.DataFrame

        # Collect data and add them to the main data frame
        result = []
        for player_data in players.itertuples(index=False):
            self.logger.info(f'Retrieving player summary data for {player_data.PERSON_ID}')

            if player_data.ROSTERSTATUS == 0:
                continue

            data = player.PlayerSummary(player_data.PERSON_ID).info()  # type: pd.DataFrame
            data_fixture = {
                "model": "main.player",
                "pk": int(data.PERSON_ID[0]),
                "fields": {
                    "team": int(data.TEAM_ID[0]),
                    "first_name": data.FIRST_NAME[0],
                    "last_name": data.LAST_NAME[0],
                    "birth_date": data.BIRTHDATE[0][:10],
                    "draft_year": data.DRAFT_YEAR[0],
                    "draft_round": data.DRAFT_ROUND[0],
                    "draft_number": data.DRAFT_NUMBER[0],
                    "position": data.POSITION[0],
                    "jersey": 0 if data.JERSEY[0] == '' else int(data.JERSEY[0]),
                    "height": data.HEIGHT[0],
                    "weight": int(data.WEIGHT[0]),
                    "school": "N/A" if data.SCHOOL[0] is None or data.SCHOOL[0] == ' ' else data.SCHOOL[0],
                    "country": data.COUNTRY[0],
                    "season_exp": int(data.SEASON_EXP[0])
                }
            }

            result.append(data_fixture)
            time.sleep(0.5)

        # Write data to file
        with open('fixtures/main_player.json', 'w+') as f:
            json.dump(result, f)

    def get_player_game_log(self) -> None:
        """Retrieve individual player game log data using API.
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
        """
        with open('data/team_list.json') as f:
            teams = json.load(f)['TEAM_ID'].values()

        all_game_log = pd.DataFrame()
        for team_id in teams:
            self.logger.info(f'Retrieving team game log data for {team_id}')

            data = team.TeamGameLogs(team_id, season=self.season).info()  # type: pd.DataFrame
            all_game_log = all_game_log.append(data, ignore_index=True)

            time.sleep(0.5)

        all_game_log.to_json(f'data/{self.season}/team_game_log.json')

    def get_team_season_stats(self) -> None:
        """Retrieve individual team season stats using API.
        """
        self.logger.info('Retrieve team season stats data.')

        data = league.TeamStats(season=self.season).overall()  # type: pd.DataFrame
        result = []
        # for team_data in data.itertuples(index=False):
        # data_fixture = {
        #     "model": "main.game",
        #     "pk": game_id,
        #     "fields": {
        #         "season": "2018-19",
        #         "game_date": parser.parse(game_summary.GAME_DATE_EST[0]).strftime("%b %d, %Y"),
        #         "dnp_players": dumps(dnp_players),
        #         "inactive_players": dumps(inactive_players),
        #         "home_team": int(game_summary.HOME_TEAM_ID[0]),
        #         "away_team": int(game_summary.VISITOR_TEAM_ID[0]),
        #         "broadcaster": broadcaster if broadcaster is not None else ''
        #     }
        # }
        # result.append(data_fixture)

        # Write data to file
        with open('fixtures/main_team_season_stats.json', 'w+') as f:
            json.dump(result, f)

    def get_boxscore_summary(self) -> None:
        """Retrieve individual game boxscore data using API.
        """
        result = []
        for game_id in [f'002180{"%04d" % index}' for index in range(1, 1231)]:
            self.logger.info(f'Retrieving boxscore data for {game_id}')

            # API calls
            player_data = game.Boxscore(game_id, season=self.season).player_stats()  # type: pd.DataFrame
            boxscore_summary = game.BoxscoreSummary(game_id, season=self.season)

            # Extract data from API responses
            game_summary = boxscore_summary.game_summary()  # type: pd.DataFrame
            broadcaster = game_summary.NATL_TV_BROADCASTER_ABBREVIATION[0]
            inactive_players = [int(data.PLAYER_ID) for data in boxscore_summary.inactive_players().itertuples()]
            dnp_players = {data.PLAYER_ID: data.COMMENT.strip() for data in player_data.itertuples()
                           if len(data.COMMENT) != 0}

            # Create fixture
            data_fixture = {
                "model": "main.game",
                "pk": game_id,
                "fields": {
                    "season": "2018-19",
                    "game_date": parser.parse(game_summary.GAME_DATE_EST[0]).strftime("%b %d, %Y"),
                    "dnp_players": json.dumps(dnp_players),
                    "inactive_players": json.dumps(inactive_players),
                    "home_team": int(game_summary.HOME_TEAM_ID[0]),
                    "away_team": int(game_summary.VISITOR_TEAM_ID[0]),
                    "broadcaster": broadcaster if broadcaster is not None else ''
                }
            }

            result.append(data_fixture)
            time.sleep(0.5)

        # Write data to file
        with open('fixtures/main_game.json', 'w+') as f:
            json.dump(result, f)


if __name__ == '__main__':
    inst = CollectData('2018-19')

    # inst.get_team_list()
    # inst.get_player_list()
    # inst.get_player_league_leader()
    # inst.get_standing_data()
    #
    # inst.get_team_summary()
    # inst.get_player_summary()
    #
    # inst.get_player_game_log()
    # inst.get_team_game_log()
    # inst.get_player_season_stats()
    # inst.get_team_season_stats()

    inst.get_boxscore_summary()
