from nba_api.stats.endpoints.leaguedashteamstats import LeagueDashTeamStats
from nba_api.stats.endpoints.leaguestandings import LeagueStandings
from nba_api.stats.endpoints.leaguegamefinder import LeagueGameFinder
from nba_api.stats.endpoints.teaminfocommon import TeamInfoCommon
from nba_api.stats.endpoints.boxscoresummaryv2 import BoxScoreSummaryV2
from pandas import DataFrame


def game_by_date_api():
    """
    Endpoint class: LeagueGameFinder()

    Endpoint fields:
        TEAM_ID, TEAM_ABBREVIATION, GAME_ID, WL, PTS
    """
    keys = [
        'GAME_DATE_EST', 'GAME_SEQUENCE', 'TEAM_CITY_NAME', 'TEAM_NICKNAME',
        'GAME_ID'
    ]
    data = LeagueGameFinder(
        league_id_nullable='00',
        date_to_nullable='06/22/2021',
        date_from_nullable='06/22/2021'
    )
    game_ids = set(data.get_data_frames()[0]['GAME_ID'])
    games = {}
    for game_id in game_ids:
        box_score: DataFrame = BoxScoreSummaryV2(game_id).get_data_frames()[5]
        box_score.drop(keys, axis=1, inplace=True)
        print(box_score.to_dict())
        games[game_id] = box_score.to_dict()

    return Response()


game_by_date_api()
