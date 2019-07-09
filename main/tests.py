"""Main App Test Module

@date: 06/02/2019
@author: Larry Shi
"""
from django.test import TestCase

from .models import Player, Team


class PlayerModelTest(TestCase):
    """Test class for <Player> model.
    """

    @classmethod
    def setUpTestData(cls):
        """Setup data for testing.
        """
        Player.objects.create(
            team=Team.objects.filter(team_abb='ATL')[0],
            first_name='a',
            last_name='b',
            birth_date='2000-01-01',
            player_id='01',
            draft_year='2019',
            draft_round='1',
            draft_number='1',
            position='Guard',
            jersey=0,
            height='5-6',
            weight=175,
            school='UCLA',
            country='USA'
        )

    def test_get_full_name(self):
        """Test <get_full_name> method in Player model.
        """
        player = Player.objects.get(id=1)
        expected_full_name = f'{player.first_name}, {player.last_name}'
        self.assertEqual(expected_full_name, player.get_full_name())

    def test_get_age(self):
        """Test <get_age> method in Player model.
        """
        player = Player.objects.get(id=1)
        expected_age = 19
        self.assertEqual(expected_age, player.get_age())


class TeamModelTest(TestCase):
    """Test class for <Team> model.
    """

    @classmethod
    def setUpTestData(cls):
        """Setup data for testing.
        """
        Team.objects.create(
            team_id='01',
            team_abb='ATL',
            team_conf='East',
            team_div='Atlantic',
            team_city='Atlanta',
            team_name='Hawks',
            wins=10,
            losses=72,
            conf_rank=2,
            div_rank=3,
            nba_debut=1968,
            season_year='2018-19'
        )

    def test_get_full_name(self):
        """Test <get_full_name> method in Team model.
        """
        team = Team.objects.get(id=1)
        expected_full_name = "Atlanta Hawks"
        self.assertEqual(expected_full_name, team.get_full_name())

    def test_get_logo_path(self):
        """Test <get_logo_path> method in Team model.
        """
        team = Team.objects.get(id=1)
        expected_logo_path = "images/ATL.png"
        self.assertEqual(expected_logo_path, team.get_logo_path())
