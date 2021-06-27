from datetime import datetime

from nba_api.stats.endpoints.boxscoresummaryv2 import BoxScoreSummaryV2
from nba_api.stats.endpoints.commonteamroster import CommonTeamRoster
from nba_api.stats.endpoints.leaguedashteamstats import LeagueDashTeamStats
from nba_api.stats.endpoints.leaguegamefinder import LeagueGameFinder
from nba_api.stats.endpoints.leaguestandings import LeagueStandings
from nba_api.stats.endpoints.teaminfocommon import TeamInfoCommon
from nba_api.stats.endpoints.teamplayerdashboard import TeamPlayerDashboard
from pandas import DataFrame
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def standings_api(request):
    """
    Endpoint class: LeagueStandings()

    Endpoint fields:
        TeamID, TeamCity, TeamName, WinPCT, WINS, LOSSES, HOME, ROAD, L10,
        ConferenceRecord, CurrentStreak, Conference, PlayoffRank, PointsPG,
        OppPointsPG, DiffPointsPG

    API fields:
        team_id, team_city, team_name, win_pct, wins, losses, home_record,
        road_record, last_ten, conference_record, curr_streak, conference, rank,
        points_pg, opp_points_pg, diff_points_pg
    """
    keys = [
        'TeamID', 'TeamCity', 'TeamName', 'WinPCT', 'WINS', 'LOSSES', 'HOME',
        'ROAD', 'L10', 'ConferenceRecord', 'CurrentStreak', 'Conference',
        'PlayoffRank', 'PointsPG', 'OppPointsPG', 'DiffPointsPG'
    ]
    standings: DataFrame = LeagueStandings().get_data_frames()[0][keys]
    standings['TeamID'] = standings['TeamID'].astype(str)
    return Response(standings.to_dict(orient='record'))


@api_view(['GET'])
def team_list_api(request):
    """
    Endpoint class: LeagueDashTeamStats()

    Endpoint fields:
        TEAM_ID, TEAM_NAME, GP, W, L, W_PCT, FGM, FGA, FG_PCT, FG3M, FG3A,
        FG3_PCT, FTM, FTA, FT_PCT, OREB, DREB, REB, AST, TOV, STL, BLK, BLKA,
        PF, PFD, PTS, PLUS_MINUS
    """
    keys = [
        'TEAM_ID', 'TEAM_NAME', 'GP', 'W', 'L', 'W_PCT', 'FGM', 'FGA', 'FG_PCT',
        'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB',
        'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PTS',
        'PLUS_MINUS'
    ]
    data = LeagueDashTeamStats(per_mode_detailed='PerGame')
    team_list: DataFrame = data.get_data_frames()[0][keys]
    team_list['TEAM_ID'] = team_list['TEAM_ID'].astype(str)

    return Response(team_list.to_dict(orient='record'))


@api_view(['GET'])
def team_detail_api(request, team_id):
    """
    Endpoint class: CommonTeamRoster(), TeamPlayerDashboard(), TeamInfoCommon()

    'players' Endpoint fields:
        PLAYER, NUM, POSITION, HEIGHT, WEIGHT, BIRTH_DATE, AGE, EXP, SCHOOL,
        PLAYER_ID

    'coaches' Endpoint fields:
        COACH_NAME, COACH_TYPE

    'team_info' Endpoint fields:
        TEAM_ID, "TEAM_CITY", TEAM_NAME, TEAM_ABBREVIATION, TEAM_CONFERENCE,
        TEAM_DIVISION, W, L, PCT, CONF_RANK, DIV_RANK, MIN_YEAR, MAX_YEAR
    """
    players_drop_keys = [
        'TeamID', 'SEASON', 'LeagueID', 'NICKNAME', 'PLAYER_SLUG'
    ]
    coaches_drop_keys = [
        'TEAM_ID', 'SEASON', 'COACH_ID', 'SORT_SEQUENCE', 'SUB_SORT_SEQUENCE',
        'IS_ASSISTANT', 'FIRST_NAME', 'LAST_NAME'
    ]
    team_info_drop_keys = [
        'SEASON_YEAR', 'TEAM_CODE', 'TEAM_SLUG'
    ]
    team_stats_keys = [
        "GP", "FGM", "FGA", "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA",
        "FT_PCT", "OREB", "DREB", "REB", "AST", "TOV", "STL", "BLK", "BLKA",
        "PF", "PFD", "PTS", "PLUS_MINUS"
    ]
    player_stats_keys = [
        "PLAYER_ID", "PLAYER_NAME", "GP", "W", "L", "MIN", "FGM", "FGA",
        "FG_PCT", "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT", "OREB",
        "DREB", "REB", "AST", "TOV", "STL", "BLK", "BLKA", "PF", "PFD", "PTS",
        "PLUS_MINUS", "DD2", "TD3"
    ]
    pct_keys = ['FG_PCT', 'FG3_PCT', 'FT_PCT']

    players, coaches = CommonTeamRoster(team_id).get_data_frames()
    players.drop(players_drop_keys, axis=1, inplace=True)
    players['AGE'] = players['AGE'].astype(int)
    coaches.drop(coaches_drop_keys, axis=1, inplace=True)

    team_info = TeamInfoCommon(team_id).get_data_frames()[0]
    team_info.drop(team_info_drop_keys, axis=1, inplace=True)
    team_info['TEAM_ID'] = team_info['TEAM_ID'].astype(str)

    team_stats, player_stats = TeamPlayerDashboard(
        team_id,
        per_mode_detailed='PerGame'
    ).get_data_frames()
    team_stats = team_stats[team_stats_keys]
    team_stats[pct_keys] = round(team_stats[pct_keys] * 100, 1)
    team_stats.rename(
        {
            'PLUS_MINUS': '+/-',
            'FG_PCT': 'FG%',
            'FG3_PCT': 'FG3%',
            'FT_PCT': 'FT%'
        },
        axis=1,
        inplace=True
    )

    player_stats = player_stats[player_stats_keys]
    player_stats[pct_keys] = round(player_stats[pct_keys] * 100, 1)
    player_stats.rename(
        {
            'PLUS_MINUS': '+/-',
            'FG_PCT': 'FG%',
            'FG3_PCT': 'FG3%',
            'FT_PCT': 'FT%'
        },
        axis=1,
        inplace=True
    )

    result = {
        'players': players.to_dict(orient='record'),
        'coaches': coaches.to_dict(orient='record'),
        'team_info': {
            key: value[0]
            for key, value in team_info.to_dict().items()
        },
        'team_stats': {
            key: value[0]
            for key, value in team_stats.to_dict().items()
        },
        'player_stats': player_stats.to_dict(orient='record')
    }
    return Response(result)


@api_view(['GET'])
def game_by_date_api(request, date):
    """
    Endpoint class: LeagueGameFinder(), BoxScoreSummaryV2()

    Endpoint fields:
        TEAM_ID, TEAM_ABBREVIATION, TEAM_WINS_LOSSES, PTS_QTR1, PTS_QTR2,
        PTS_QTR3, PTS_QTR4, PTS_OT1, PTS_OT2, PTS_OT3, PTS_OT4, PTS_OT5,
        PTS_OT6, PTS_OT7, PTS_OT8, PTS_OT9, PTS_OT10, PTS

    Date format: 2021-06-24 (%Y-%m-%d)
    """
    line_score_drop_keys = [
        'GAME_DATE_EST', 'GAME_SEQUENCE', 'TEAM_CITY_NAME', 'TEAM_NICKNAME',
        'GAME_ID'
    ]
    broadcast_keys = [
        'GAME_STATUS_TEXT', 'NATL_TV_BROADCASTER_ABBREVIATION', 'LIVE_PERIOD'
    ]

    parsed_date = datetime.strptime(date, '%Y-%m-%d').strftime('%m/%d/%Y')
    data = LeagueGameFinder(
        league_id_nullable='00',
        date_to_nullable=parsed_date,
        date_from_nullable=parsed_date
    )

    games = data.get_data_frames()[0]
    games_summary = {}
    for game_id in set(games['GAME_ID']):
        box_score = BoxScoreSummaryV2(game_id).get_data_frames()
        line_score: DataFrame = box_score[5]
        line_score.drop(line_score_drop_keys, axis=1, inplace=True)
        line_score['TEAM_ID'] = line_score['TEAM_ID'].astype(str)
        broadcast: DataFrame = box_score[0][broadcast_keys].iloc[0]
        games_summary[game_id] = {
            'line_score': line_score.to_dict(orient='record'),
            'broadcast': broadcast.to_dict()
        }

    return Response(games_summary)
