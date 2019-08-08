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

        # ======================================================================
        # Data Attributes
        # ======================================================================
        # Team List
        self.logger.info(f'Retrieving team list data')
        self.team_list = team.TeamList().info()[['TEAM_ID']][:30]

        # Player List
        self.logger.info('Retrieving player list data')
        self.player_list = player.PlayerList(season=self.season).info()[['PERSON_ID', 'ROSTERSTATUS']]

        # Standing Data
        self.logger.info('Retrieving standing data')
        year = int(f'20{self.season.split("-")[1]}')
        data = pd.DataFrame()
        data = data.append(Scoreboard(month=6, day=1, year=year).east_conf_standings_by_day(), ignore_index=True)
        data = data.append(Scoreboard(month=6, day=1, year=year).west_conf_standings_by_day(), ignore_index=True)
        self.standing_data = data

        # Team Summary
        self.team_summary = pd.DataFrame()
        for team_data in self.team_list.itertuples(index=False):
            self.logger.info(f'Retrieving team summary data for {team_data.TEAM_ID}')

            data = team.TeamSummary(team_data.TEAM_ID, season=self.season).info()
            self.team_summary = self.team_summary.append(data, ignore_index=True)

        # Player Summary
        self.player_summary = pd.DataFrame()
        for player_data in self.player_list.itertuples(index=False):
            self.logger.info(f'Retrieving player summary data for {player_data.PERSON_ID}')

            if player_data.ROSTERSTATUS == 0:
                continue

            data = player.PlayerSummary(player_data.PERSON_ID).info()
            self.player_summary = self.player_summary.append(data, ignore_index=True)

        # Player Game Log
        self.logger.info('Retrieving player game log data.')
        self.player_game_log = league.GameLog(
            season=self.season,
            player_or_team=Player_or_Team.Player
        ).overall().round(3)
        self.player_game_log.fillna(0, inplace=True)

        # Team Season Stats
        self.logger.info('Retrieve team season stats data.')
        self.team_season_stats = league.TeamStats(season=self.season).overall().round(3)

        # Boxscore
        self.boxscore_data = {}
        for game_id in [f'002180{"%04d" % index}' for index in range(1, 1231)]:
            self.logger.info(f'Retrieving boxscore data for {game_id}')

            player_data = game.Boxscore(game_id, season=self.season).player_stats()

            boxscore_summary = game.BoxscoreSummary(game_id, season=self.season)
            game_summary = boxscore_summary.game_summary()
            inactive_players = boxscore_summary.inactive_players()
            line_score = boxscore_summary.line_score()

            self.boxscore_data[game_id] = {
                'player_data': player_data,
                'game_summary': game_summary,
                'inactive_players': inactive_players,
                'line_score': line_score
            }

        # Team Game Log
        self.team_game_log = pd.DataFrame()
        for team_id in self.team_list:
            self.logger.info(f'Retrieving team game log data for {team_id}')

            data = team.TeamGameLogs(team_id, season=self.season).info()
            self.team_game_log = self.team_game_log.append(data, ignore_index=True)

    def get_standing_data(self) -> None:
        """Retrieve season standing data using API.
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

    def get_team_summary(self) -> None:
        """Retrieve individual team summary data using API.
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
                "max_year": "2018-19"
            }
        })

        # Write data to file
        with open('fixtures/main_team.json', 'w+') as f:
            json.dump(result, f)

    def get_player_summary(self) -> None:
        """Retrieve individual player summary data using API.
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

    def get_player_game_log(self) -> None:
        """Retrieve individual player game log data using API.
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

    def get_team_season_stats(self) -> None:
        """Retrieve individual team season stats using API.
        """
        result = []
        for team_data in self.team_season_stats.itertuples():
            data_fixture = {
                "model": "main.teamseasonstats",
                "pk": team_data.Index + 1,
                "fields": {
                    "minutes": team_data.MIN,
                    "points": team_data.PTS,
                    "offense_reb": team_data.OREB,
                    "defense_reb": team_data.DREB,
                    "rebounds": team_data.REB,
                    "assists": team_data.AST,
                    "steals": team_data.STL,
                    "blocks": team_data.BLK,
                    "turnovers": team_data.TOV,
                    "fouls": team_data.PF,
                    "fg_made": team_data.FGM,
                    "fg_attempt": team_data.FGA,
                    "fg_percent": team_data.FG_PCT,
                    "fg3_made": team_data.FG3M,
                    "fg3_attempt": team_data.FG3A,
                    "fg3_percent": team_data.FG3_PCT,
                    "ft_made": team_data.FTM,
                    "ft_attempt": team_data.FTA,
                    "ft_percent": team_data.FT_PCT,
                    "season": "2018-19",
                    "team": team_data.TEAM_ID,
                    "wins": team_data.W,
                    "losses": team_data.L,
                    "win_percent": team_data.W_PCT
                }
            }
            result.append(data_fixture)

        # Write data to file
        with open('fixtures/main_team_season_stats.json', 'w+') as f:
            json.dump(result, f)

    def get_boxscore_summary(self) -> None:
        """Retrieve individual game boxscore data using API.
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
