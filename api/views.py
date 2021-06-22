from nba_api.stats.endpoints.leaguestandings import LeagueStandings
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
    # key_field_map = {
    #     'TeamID': 'team_id',
    #     'TeamCity': 'team_city',
    #     'TeamName': 'team_name',
    #     'WinPCT': 'win_pct',
    #     'WINS': 'wins',
    #     'LOSSES': 'losses',
    #     'HOME': 'home_record',
    #     'ROAD': 'road_record',
    #     'L10': 'last_ten',
    #     'ConferenceRecord': 'conference_record',
    #     'CurrentStreak': 'curr_streak',
    #     'Conference': 'conference',
    #     'PlayoffRank': 'rank',
    #     'PointsPG': 'points_pg',
    #     'OppPointsPG': 'opp_points_pg',
    #     'DiffPointsPG': 'diff_points_pg'
    # }
    standings = LeagueStandings().get_data_frames()[0][keys]
    # standings = data.rename(columns=key_field_map)
    standings['TeamID'] = standings['TeamID'].astype(str)

    # serializer = StandingsSerializer(data=standings, many=True)
    # if not serializer.is_valid():
    #     return Response(serializer.errors)

    # return Response(serializer.data)
    return Response(standings.to_dict(orient='record'))
