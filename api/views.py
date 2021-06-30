from datetime import datetime

import numpy
import simplejson
from dateutil import parser
from nba_api.stats.endpoints.boxscoresummaryv2 import BoxScoreSummaryV2
from nba_api.stats.endpoints.boxscoretraditionalv2 import BoxScoreTraditionalV2
from nba_api.stats.endpoints.commonplayerinfo import CommonPlayerInfo
from nba_api.stats.endpoints.commonteamroster import CommonTeamRoster
from nba_api.stats.endpoints.leaguedashteamstats import LeagueDashTeamStats
from nba_api.stats.endpoints.leaguegamefinder import LeagueGameFinder
from nba_api.stats.endpoints.leaguestandings import LeagueStandings
from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats
from nba_api.stats.endpoints.teaminfocommon import TeamInfoCommon
from nba_api.stats.endpoints.teamplayerdashboard import TeamPlayerDashboard
from pandas import DataFrame
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Constants
PLAYER_PHOTO_LINK = "https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png"


# Encoder
def converter(obj):
    if isinstance(obj, numpy.integer):
        return int(obj)
    elif isinstance(obj, numpy.floating):
        return float(obj)
    elif isinstance(obj, numpy.ndarray):
        return obj.tolist()

    raise TypeError(repr(obj) + " is not JSON serializable")


# Util functions
def update_fields(df: DataFrame, single_game: bool = False) -> DataFrame:
    """Convert pct fields from 0.xxx to xx.x format and update certain keys
    names to display names.
    """
    # Update percentage fields
    keys = [
        'FG_PCT', 'FG3_PCT', 'FT_PCT', 'WIN_PCT', 'WinPCT', 'W_PCT'
    ]
    result = df.copy()
    for key in keys:
        if key in df.keys():
            result[key] = round(100 * result[key], 1)

    # Change team id type to string
    team_id_keys = ['TEAM_ID', 'TeamID']
    for key in team_id_keys:
        if key in df.keys():
            result[key] = result[key].astype(str)

    # Update single game stat fields if enabled
    if single_game:
        clean_single_game_data(result)

    # Rename fields for display purpose
    mapping = {
        'PLUS_MINUS': '+/-',
        'FG_PCT': 'FG%',
        'FG3_PCT': 'FG3%',
        'FT_PCT': 'FT%',
        'WIN_PCT': 'WIN%',
        'W_PCT': 'WIN%',
        'START_POSITION': 'P'
    }
    for key, value in mapping.items():
        if key in df.keys():
            result.rename({key: value}, axis=1, inplace=True)

    return result


def clean_single_game_data(df: DataFrame) -> None:
    float_fields = ['FG_PCT', 'FG3_PCT', 'FT_PCT']
    ignore_fields = [
        'TEAM_ID', 'PLAYER_ID', 'PLAYER_NAME', 'START_POSITION', 'COMMENT'
    ]
    time_fields = ['MIN']
    for index, row in df.iterrows():
        if row['MIN'] is None:
            for key, value in row.items():
                if key in float_fields:
                    row[key] = 0.0
                elif key in time_fields:
                    row[key] = '00:00'
                elif key not in ignore_fields:
                    row[key] = 0

        df.iloc[index] = row

    for col_type, key in zip(df.dtypes, df.keys()):
        if key not in ignore_fields and key not in float_fields and \
                key not in time_fields:
            df[key] = df[key].astype(int)


# API views
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
    standings = update_fields(LeagueStandings().standings.get_data_frame()[keys])

    return Response(standings.to_dict(orient='records'))


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
    data = update_fields(LeagueDashTeamStats(per_mode_detailed='PerGame').league_dash_team_stats.get_data_frame()[keys])
    return Response(data.to_dict(orient='records'))


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
    roster_data = CommonTeamRoster(team_id)
    players = roster_data.common_team_roster.get_data_frame().drop(players_drop_keys, axis=1)
    players['AGE'] = players['AGE'].astype(int)
    coaches = roster_data.coaches.get_data_frame().drop(coaches_drop_keys, axis=1)

    team_info_drop_keys = [
        'SEASON_YEAR', 'TEAM_CODE', 'TEAM_SLUG'
    ]
    team_info = TeamInfoCommon(team_id).team_info_common.get_data_frame().drop(team_info_drop_keys, axis=1)
    team_info['TEAM_ID'] = team_info['TEAM_ID'].astype(str)

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
    team_stats, player_stats = TeamPlayerDashboard(team_id, per_mode_detailed='PerGame').get_data_frames()
    team_stats = update_fields(team_stats[team_stats_keys])
    player_stats = update_fields(player_stats[player_stats_keys])

    result = {
        'players': players.to_dict(orient='records'),
        'coaches': coaches.to_dict(orient='records'),
        'team_info': {
            key: value[0]
            for key, value in team_info.to_dict().items()
        },
        'team_stats': {
            key: value[0]
            for key, value in team_stats.to_dict().items()
        },
        'player_stats': player_stats.to_dict(orient='records')
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

    parsed_date = parser.parse(date).strftime('%m/%d/%Y')
    data = LeagueGameFinder(
        league_id_nullable='00',
        date_to_nullable=parsed_date,
        date_from_nullable=parsed_date
    )

    games = data.league_game_finder_results.get_data_frame()
    games_summary = {}
    for game_id in set(games['GAME_ID']):
        box_score = BoxScoreSummaryV2(game_id)
        line_score = box_score.line_score.get_data_frame().drop(line_score_drop_keys, axis=1)
        line_score['TEAM_ID'] = line_score['TEAM_ID'].astype(str)
        broadcast = box_score.game_summary.get_data_frame()[broadcast_keys]
        games_summary[game_id] = {
            'line_score': line_score.to_dict(orient='records'),
            'broadcast': broadcast.iloc[0].to_dict()
        }

    return Response(games_summary)


@api_view(['GET'])
def game_by_id_api(request, game_id):
    """
    Endpoint class: BoxScoreTraditionalV2(), BoxScoreSummaryV2()
    """
    # Get box score summary
    line_score_drop_keys = [
        'GAME_DATE_EST', 'GAME_SEQUENCE', 'TEAM_CITY_NAME', 'TEAM_NICKNAME',
        'GAME_ID'
    ]
    summary_keys = [
        'GAME_STATUS_TEXT', 'NATL_TV_BROADCASTER_ABBREVIATION', 'LIVE_PERIOD',
        'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'GAME_DATE_EST'
    ]
    inactive_drop_keys = [
        'TEAM_CITY', 'TEAM_NAME'
    ]
    box_score = BoxScoreSummaryV2(game_id)
    summary = box_score.game_summary.get_data_frame()[summary_keys].iloc[0]
    summary['HOME_TEAM_ID'] = summary['HOME_TEAM_ID'].astype(str)
    summary['VISITOR_TEAM_ID'] = summary['VISITOR_TEAM_ID'].astype(str)

    line_score = update_fields(box_score.line_score.get_data_frame().drop(line_score_drop_keys, axis=1))
    inactive_players = update_fields(box_score.inactive_players.get_data_frame().drop(inactive_drop_keys, axis=1))

    # Get traditional box score data
    player_stats_drop_keys = [
        'GAME_ID', 'TEAM_CITY', 'TEAM_ABBREVIATION', 'NICKNAME'
    ]
    team_stats_drop_keys = [
        'GAME_ID', 'TEAM_ABBREVIATION'
    ]
    box_score_trad = BoxScoreTraditionalV2(game_id)
    player_stats = update_fields(
        box_score_trad.player_stats.get_data_frame().drop(player_stats_drop_keys, axis=1),
        single_game=True
    )
    team_stats = update_fields(box_score_trad.team_stats.get_data_frame().drop(team_stats_drop_keys, axis=1))

    # Split data to two teams
    overtime_keys = [
        f'PTS_OT{i}' for i in range(1, 11)
    ]
    home_team_id = summary['HOME_TEAM_ID']
    home_line_score = line_score[line_score['TEAM_ID'] == home_team_id].iloc[0]
    home_team_data = {
        'player_stats': [],
        'line_score': home_line_score.drop(overtime_keys).to_dict(),
        'team_stats': team_stats[team_stats['TEAM_ID'] == home_team_id].iloc[0].to_dict()
    }

    away_team_id = summary['VISITOR_TEAM_ID']
    away_line_score = line_score[line_score['TEAM_ID'] == away_team_id].iloc[0]
    away_team_data = {
        'player_stats': [],
        'line_score': away_line_score.drop(overtime_keys).to_dict(),
        'team_stats': team_stats[team_stats['TEAM_ID'] == away_team_id].iloc[0].to_dict()
    }

    for _, row in player_stats.iterrows():
        if row.get('TEAM_ID') == home_team_id:
            home_team_data['player_stats'].append(row.to_dict())
        elif row.get('TEAM_ID') == away_team_id:
            away_team_data['player_stats'].append(row.to_dict())

    overtime = {
        i: {
            'flag': False if i > summary['LIVE_PERIOD'] - 4 else True,
            'home': home_line_score[overtime_keys].iloc[i - 1],
            'away': away_line_score[overtime_keys].iloc[i - 1]
        }
        for i in range(1, 11)
    }

    # Return JSON response
    result = {
        'summary': summary.to_dict(),
        'inactive_players': inactive_players.to_dict(orient='records'),
        'overtime': overtime,
        'home_team': home_team_data,
        'away_team': away_team_data
    }
    date = parser.parse(result['summary']['GAME_DATE_EST'])
    result['summary']['GAME_DATE_EST'] = date.strftime('%B %d, %Y')

    home_pts = line_score[line_score['TEAM_ID'] == home_team_id].iloc[0]['PTS']
    away_pts = line_score[line_score['TEAM_ID'] == away_team_id].iloc[0]['PTS']
    result['summary']['HOME_WON'] = bool(home_pts > away_pts)

    serialized = simplejson.dumps(result, ignore_nan=True, default=converter)
    return Response(simplejson.loads(serialized))


@api_view(['GET'])
def player_detail_api(request, player_id):
    """
    Endpoint class:
    """
    player_info_keys = [
        'DISPLAY_FIRST_LAST', 'BIRTHDATE', 'SCHOOL', 'COUNTRY', 'HEIGHT',
        'WEIGHT', 'SEASON_EXP', 'JERSEY', 'POSITION', 'TEAM_NAME', 'TEAM_CITY',
        'FROM_YEAR', 'TEAM_ID', 'DRAFT_ROUND', 'DRAFT_NUMBER', 'PERSON_ID'
    ]
    player_info = CommonPlayerInfo(player_id).common_player_info.get_data_frame().iloc[0][player_info_keys]
    player_info['BIRTHDATE'] = parser.parse(player_info['BIRTHDATE']).strftime('%Y-%m-%d')
    player_info['PHOTO_URL'] = PLAYER_PHOTO_LINK.format(player_id=player_id)
    player_info['AGE'] = datetime.today().year - parser.parse(player_info['BIRTHDATE']).year

    career_drop_keys = [
        'PLAYER_ID', 'LEAGUE_ID', 'Team_ID'
    ]
    season_drop_keys = [
        'PLAYER_ID', 'LEAGUE_ID', 'PLAYER_AGE'
    ]
    career_stats = PlayerCareerStats(player_id, per_mode36='PerGame')
    career_regular_season = career_stats.career_totals_regular_season.get_data_frame().iloc[0].drop(career_drop_keys)
    career_regular_season = update_fields(career_regular_season)
    career_post_season = career_stats.career_totals_post_season.get_data_frame().iloc[0].drop(career_drop_keys)
    career_post_season = update_fields(career_post_season)
    regular_season = career_stats.season_totals_regular_season.get_data_frame().drop(season_drop_keys, axis=1)
    regular_season = update_fields(regular_season)
    post_season = career_stats.season_totals_post_season.get_data_frame().drop(season_drop_keys, axis=1)
    post_season = update_fields(post_season)

    result = {
        'player_info': player_info.to_dict(),
        'stats': {
            'regular_season': {
                'display_name': "Regular",
                'season': regular_season.iloc[::-1].to_dict(orient='records'),
                'career': career_regular_season.to_dict()
            },
            'post_season': {
                'display_name': "Post",
                'season': post_season.iloc[::-1].to_dict(orient='records'),
                'career': career_post_season.to_dict()
            }
        }
    }
    return Response(result)
