"""

@date: 08/07/2019
@author: Larry Shi
"""
from rest_framework import serializers

from main.models import Team


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = '__all__'
