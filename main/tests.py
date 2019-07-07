"""Main App Test Module

@date: 06/02/2019
@author: Larry Shi
"""
from django.test import TestCase

from .models import Player, Team


class PlayerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
        player = Player.objects.get(id=1)
        expected_full_name = f'{player.first_name}, {player.last_name}'
        self.assertEqual(expected_full_name, player.get_full_name())

    def test_get_age(self):
        player = Player.objects.get(id=1)
        expected_age = 19
        self.assertEqual(expected_age, player.get_age())
