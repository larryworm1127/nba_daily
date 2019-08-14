"""

@date: 08/07/2019
@author: Larry Shi
"""
from rest_framework import serializers

from main.models import Team


class TeamSerializer(serializers.ModelSerializer):
    season_stats = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='season'
    )
    # standing = serializers.RelatedField(read_only=True)

    class Meta:
        model = Team
        fields = ['team_abb', 'season_stats']
