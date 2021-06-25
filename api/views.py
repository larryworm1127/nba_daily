from datetime import datetime

from nba_api.stats.endpoints.boxscoresummaryv2 import BoxScoreSummaryV2
from nba_api.stats.endpoints.leaguedashteamstats import LeagueDashTeamStats
from nba_api.stats.endpoints.leaguegamefinder import LeagueGameFinder
from nba_api.stats.endpoints.leaguestandings import LeagueStandings
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
def game_by_date_api(request, date):
    """
    Endpoint class: LeagueGameFinder()

    Endpoint fields:
        TEAM_ID, TEAM_ABBREVIATION, TEAM_WINS_LOSSES, PTS_QTR1, PTS_QTR2,
        PTS_QTR3, PTS_QTR4, PTS_OT1, PTS_OT2, PTS_OT3, PTS_OT4, PTS_OT5,
        PTS_OT6, PTS_OT7, PTS_OT8, PTS_OT9, PTS_OT10, PTS

    Date format: 2021-06-24 (%Y-%m-%d)
    """
    line_score_keys = [
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
        line_score.drop(line_score_keys, axis=1, inplace=True)
        line_score['TEAM_ID'] = line_score['TEAM_ID'].astype(str)
        broadcast: DataFrame = box_score[0][broadcast_keys].iloc[0]
        games_summary[game_id] = {
            'line_score': line_score.to_dict(orient='record'),
            'broadcast': broadcast.to_dict()
        }

    return Response(games_summary)
