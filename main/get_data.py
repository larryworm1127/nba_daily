"""

@date: 07/07/2019
@author: Larry Shi
"""
import logging
import os
import time

import pandas as pd
from nba_py import game, team, player, league
from nba_py.constants import Player_or_Team
from simplejson import load, dump


def get_team_list() -> None:
    """Retrieve team list data using API.
    """
    logging.info(f'Retrieving team list data')

    team_list = team.TeamList().info()
    team_list.to_json('data/team_list.json')


def get_player_list(season: str) -> None:
    """Retrieve player list data using API.

    === Attributes ===
    season:
        the season to get the player list from.
    """
    logging.info('Retrieving player list data')

    player_list = player.PlayerList(season=season).info()
    player_list.to_json(f'data/{season}/player_list.json')


def get_player_league_leader(season: str) -> None:
    """Retrieve player league leader data using API.

    === Attributes ===
    season:
        the season to get the league leader data from.
    """
    logging.info('Retrieve league leader data')

    leaders = league.Leaders(stat_category="EFF", season=season).results()
    leaders.to_json(f'data/{season}/player_leaders.json')


def get_team_summary(season: str) -> None:
    """Retrieve individual team summary data using API.

    === Attributes ===
    season:
        the season to get the team summary from.
    """
    with open('data/team_list.json') as f:
        teams = load(f)

    team_summ = pd.DataFrame()
    for team_id in teams['TEAM_ID'].values():
        logging.info(f'Retrieving team summary data for {team_id}')

        data = team.TeamSummary(team_id, season=season).info()  # type: pd.DataFrame
        team_summ = team_summ.append(data, ignore_index=True)

        time.sleep(1)

    team_summ = team_summ.drop(columns=['SEASON_YEAR', 'TEAM_CODE', 'PCT', 'CONF_RANK', 'DIV_RANK'])
    team_summ.to_json('data/team_summary.json')


def get_player_summary() -> None:
    """Retrieve individual player summary data using API.
    """
    with open('data/2018-19/player_list.json') as f:
        players = load(f)

    for index, player_id in enumerate(players['PERSON_ID'].values()):
        logging.info(f'Retrieving player summary data for {player_id}')

        if list(players['TEAM_ID'].values())[index] == 0:
            continue

        data = player.PlayerSummary(player_id).info()
        data.to_json(f'data/player_summary/{player_id}.json')

        time.sleep(1)

    assert len(os.listdir('data/player_summary')) == 483


def get_player_game_stats(season: str) -> None:
    """Retrieve individual player game log data using API.

    === Attributes ===
    season:
        the season to get the player game log from.
    """
    logging.info('Retrieving player game log data.')

    data = league.GameLog(season=season, player_or_team=Player_or_Team.Player).overall()
    data.fillna(0, inplace=True)
    data.to_json(f'data/{season}/player_game_log.json')

    data = league.PlayerStats(season=season).overall()
    data.to_json(f'data/{season}/player_stats.json')


def get_team_game_stats(season: str) -> None:
    """Retrieve individual team game log data using API.

    === Attributes ===
    season:
        the season to get the team game log from.
    """
    with open('data/team_list.json') as f:
        teams = load(f)['TEAM_ID'].values()

    all_game_log = pd.DataFrame()
    for team_id in teams:
        logging.info(f'Retrieving team game log data for {team_id}')

        data = team.TeamGameLogs(team_id, season=season).info()  # type: pd.DataFrame
        all_game_log = all_game_log.append(data, ignore_index=True)

        time.sleep(1)

    all_game_log.to_json(f'data/{season}/team_game_log.json')

    data = league.TeamStats(season=season).overall()
    data.to_json(f'data/{season}/team_stats.json')


def get_game_list(season: str) -> None:
    """Retrieve game list data from team game log.

    === Attributes ===
    season:
        the season in which the games are played.
    """
    logging.info('Retrieving game list data')

    with open('data/team_list.json') as f:
        teams = load(f)['TEAM_ID'].values()

    games = set([])
    for team_id in teams:
        with open(f'data/team_game_log/{season}/{team_id}.json') as f:
            game_log = load(f)

        for game_id in game_log.get("Game_ID").values():
            games.add(game_id)

    with open('data/game_list.json', 'w+') as f:
        dump(list(games), f)


def get_box_score(season: str) -> None:
    """Retrieve individual game player box score data using API.

    === Attributes ===
    season:
        the season in which the games are played.
    """
    with open('data/game_list.json') as f:
        games = load(f)

    for game_id in games:
        logging.info(f'Retrieving box score data for {game_id}')
        data = game.Boxscore(game_id, season=season).player_stats()
        data.to_json(f'data/boxscore/{season}/{game_id}.json')

        time.sleep(1)

    assert len(os.listdir(f'data/boxscore/{season}')) == 1230


def get_box_score_summary(season: str) -> None:
    """Retrieve individual game box score summary data using API.

    === Attributes ===
    season:
        the season in which the games are played.
    """
    with open('data/game_list.json') as f:
        games = load(f)

    temp = games.index('0021800797')

    for game_id in games[temp:]:
        logging.info(f'Retrieving box score summary data for {game_id}')

        data = game.BoxscoreSummary(game_id, season=season)
        game_summary = data.game_summary()
        game_summary.to_json(f'data/boxscore_summary/{season}/game_summary/{game_id}.json')

        line_score = data.line_score()
        line_score.to_json(f'data/boxscore_summary/{season}/line_score/{game_id}.json')

        inactive_player = data.inactive_players()
        inactive_player.to_json(f'data/boxscore_summary/{season}/inactive_players/{game_id}.json')

        time.sleep(1)

    assert len(os.listdir(f'data/boxscore_summary/{season}/line_score')) == 1230
    assert len(os.listdir(f'data/boxscore_summary/{season}/game_summary')) == 1230
    assert len(os.listdir(f'data/boxscore_summary/{season}/inactive_players')) == 1230


if __name__ == '__main__':
    # Configure logger
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt='%Y/%m/%d %I:%M:%S',
        level=logging.DEBUG
    )

    season_year = '2018-19'

    # get_team_list()
    # get_player_list(season_year)
    # get_player_league_leader(season_year)

    get_team_summary(season_year)
    # get_player_summary()

    # get_player_game_stats(season_year)
    # get_team_game_stats(season_year)

    # get_game_list(season_year)
    # get_box_score(season_year)
    # get_box_score_summary(season_year)
