"""

@date: 07/07/2019
@author: Larry Shi
"""
import time
import logging

from simplejson import load
from nba_py import game, team, player


def get_team_list() -> None:
    """Retrieve team list data using API.
    """
    logging.info(f'Retrieving team list data')

    team_list = team.TeamList().info()
    team_list.to_json('data/team_list.json')


def get_player_list(season: str = '2018-19') -> None:
    """Retrieve player list data using API.

    === Attributes ===
    season:
        the season to get the player list from.
    """
    logging.info(f'Retrieving player list data')

    player_list = player.PlayerList(season=season).info()
    player_list.to_json('data/player_list.json')


def get_player_game_log(season: str = '2018-19') -> None:
    """Retrieve individual player game log data using API.

    === Attributes ===
    season:
        the season to get the player game log from.
    """
    with open('data/player_list.json') as f:
        players = load(f)['PERSON_ID'].values()

    for player_id in players:
        print(player_id)
        logging.info(f'Retrieving player game log data for {player_id}')

        data = player.PlayerGameLogs(player_id, season=season).info()
        data.to_json(f'data/player_game_log/{season}/{player_id}.json')

        time.sleep(1)


def get_team_game_log(season: str = '2018-19') -> None:
    """Retrieve individual team game log data using API.

    === Attributes ===
    season:
        the season to get the team game log from.
    """
    with open('data/team_list.json') as f:
        teams = load(f)['TEAM_ID'].values()

    for team_id in teams:
        print(team_id)
        logging.info(f'Retrieving team game log data for {team_id}')

        data = player.PlayerGameLogs(team_id, season=season).info()
        data.to_json(f'data/team_game_log/{season}/{team_id}.json')

        time.sleep(1)


if __name__ == '__main__':
    # Configure logger
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y/%m/%d %I:%M:%S',
        level=logging.DEBUG
    )

    # get_team_list()
    # get_player_list()

    get_team_list()
    get_player_game_log()
