"""Main App Test Module

@date: 06/02/2019
@author: Larry Shi
"""
import re

from datetime import date, datetime

from hypothesis import given
from hypothesis.extra.django import TestCase
from hypothesis.strategies import from_regex, dates

from .models import Player, Team


# Constants
NAME_REGEX = re.compile(r'[a-zA-Z]{2,15}')
ABB_REGEX = re.compile(r'[a-zA-Z]{3}')


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
            player_id=1,
            draft_year='2019',
            draft_round='1',
            draft_number='1',
            position='Guard',
            jersey=0,
            height='5-6',
            weight=175,
            school='UCLA',
            country='USA',
            season_exp=1
        )

    @given(from_regex(NAME_REGEX, fullmatch=True), from_regex(NAME_REGEX, fullmatch=True))
    def test_get_full_name(self, first_name: str, last_name: str):
        """Test <get_full_name> method in Player model.
        """
        player = Player.objects.get(player_id=1)
        player.first_name = first_name
        player.last_name = last_name
        expected_full_name = f'{first_name} {last_name}'
        self.assertEqual(expected_full_name, player.get_full_name())

    @given(dates(min_value=date(1980, 1, 1), max_value=date(2000, 12, 31)))
    def test_get_age(self, birth_date: date):
        """Test <get_age> method in Player model.
        """
        player = Player.objects.get(player_id=1)
        player.birth_date = str(birth_date)
        expected_age = datetime.today().year - birth_date.year
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
            season='2018-19'
        )

    @given(from_regex(NAME_REGEX, fullmatch=True), from_regex(NAME_REGEX, fullmatch=True))
    def test_get_full_name(self, team_city: str, team_name: str):
        """Test <get_full_name> method in Team model.
        """
        team = Team.objects.get(id=1)
        team.team_city = team_city
        team.team_name = team_name
        expected_full_name = f'{team_city} {team_name}'
        self.assertEqual(expected_full_name, team.get_full_name())

    @given(from_regex(ABB_REGEX, fullmatch=True))
    def test_get_logo_path(self, team_abb: str):
        """Test <get_logo_path> method in Team model.
        """
        team = Team.objects.get(id=1)
        team.team_abb = team_abb
        expected_logo_path = f"images/{team_abb}.png"
        self.assertEqual(expected_logo_path, team.get_logo_path())
