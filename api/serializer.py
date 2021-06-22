from rest_framework import serializers


class StandingsSerializer(serializers.Serializer):
    """Serializer for standings data.

    Fields:
        team_city, team_name, win_pct, wins, losses, home_record, road_record,
        last_ten, conference_record, curr_streak, conference, rank, points_pg,
        opp_points_pg, diff_points_pg
    """
    team_id = serializers.CharField()
    team_city = serializers.CharField()
    team_name = serializers.CharField()
    win_pct = serializers.FloatField(min_value=0.0)
    wins = serializers.IntegerField(min_value=0)
    losses = serializers.IntegerField(min_value=0)
    home_record = serializers.CharField(max_length=5)
    road_record = serializers.CharField(max_length=5)
    last_ten = serializers.CharField(max_length=4)
    conference_record = serializers.CharField(max_length=5)
    curr_streak = serializers.IntegerField()
    conference = serializers.CharField(max_length=4)
    rank = serializers.IntegerField(min_value=1)
    points_pg = serializers.FloatField(min_value=0.0)
    opp_points_pg = serializers.FloatField(min_value=0.0)
    diff_points_pg = serializers.FloatField()
