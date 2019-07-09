"""

@date: 07/07/2019
@author: Larry Shi
"""
import logging
import os
import time

from nba_py import game, team, player
from simplejson import load


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
        players = load(f)

    for index, player_id in enumerate(players['PERSON_ID'].values()):
        logging.info(f'Retrieving player game log data for {player_id}')

        if list(players['TEAM_ID'].values())[index] == 0:
            continue

        data = player.PlayerGameLogs(player_id, season=season).info()
        data.to_json(f'data/player_game_log/{season}/{player_id}.json')

        time.sleep(1)

    assert len(os.listdir(f'data/player_game_log/{season}')) == 483


def get_player_summary() -> None:
    """Retrieve individual player summary data using API.
    """
    with open('data/player_list.json') as f:
        players = load(f)

    for index, player_id in enumerate(players['PERSON_ID'].values()):
        logging.info(f'Retrieving player summary data for {player_id}')

        if list(players['TEAM_ID'].values())[index] == 0:
            continue

        data = player.PlayerSummary(player_id).info()
        data.to_json(f'data/player_summary/{player_id}.json')

        time.sleep(1)

    assert len(os.listdir(f'data/player_summary/')) == 483


def get_team_game_log(season: str = '2018-19') -> None:
    """Retrieve individual team game log data using API.

    === Attributes ===
    season:
        the season to get the team game log from.
    """
    with open('data/team_list.json') as f:
        teams = load(f)['TEAM_ID'].values()

    for team_id in teams:
        logging.info(f'Retrieving team game log data for {team_id}')

        data = team.TeamGameLogs(team_id, season=season).info()
        data.to_json(f'data/team_game_log/{season}/{team_id}.json')

        time.sleep(1)

    assert len(os.listdir(f'data/team_game_log/{season}')) == 30


def get_box_score(season: str = '2018-19') -> None:
    """Retrieve individual game player box score data using API.

    === Attributes ===
    season:
        the season in which the games are played.
    """
    with open('data/team_list.json') as f:
        teams = load(f)['TEAM_ID'].values()

    games = set([])
    for team_id in teams:
        with open(f'data/team_game_log/{season}/{team_id}.json') as f:
            game_log = load(f)

        for game_id in game_log.get("Game_ID").values():
            games.add(game_id)

    for game_id in games:
        logging.info(f'Retrieving box score data for {game_id}')
        data = game.Boxscore(game_id).player_stats()
        data.to_json(f'data/boxscore/{season}/{game_id}.json')

        time.sleep(1)

    assert len(os.listdir(f'data/boxscore/{season}')) == 1230


g = [1626187, 1628500, 1626780, 203460, 1629008, 1629117, 1629129, 1629134, 1629341, 204001, 1627738, 1627749, 1627756, 1627785, 202389]

if __name__ == '__main__':
    # Configure logger
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y/%m/%d %I:%M:%S',
        level=logging.DEBUG
    )

    # get_team_list()
    # get_player_list()

    # get_player_game_log()
    # get_team_game_log()
    # get_player_summary()
    get_box_score()
