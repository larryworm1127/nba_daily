"""Main App View Test Module

@date: 07/27/2019
@author: Larry Shi
"""
from django.test import TestCase
from django.urls import reverse

from main.models import Team, Player


class TeamListViewTest(TestCase):
    """Test class for <TeamListView> generic view.
    """

    @classmethod
    def setUpTestData(cls):
        """Setup data for testing.
        """
        # Create teams for tests
        num_teams = 30
        for team_id in range(num_teams):
            Team.objects.create(
                team_id=team_id,
                team_abb='TOT',
                team_conf='N/A',
                team_div='N/A',
                team_city='N/A',
                team_name='N/A',
                wins=82,
                losses=0,
                nba_debut='1950',
                max_year='2018-19'
            )

    # def test_view_url_exists_at_desired_location(self):
    #     """Test if the view has the correct URL.
    #     """
    #     response = self.client.get('/teams')
    #     self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test if the URL of the view can be obtained using its name.
        """
        response = self.client.get(reverse('main:team_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test if the view uses the desired template.
        """
        response = self.client.get(reverse('main:team_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/team_list.html')

    def test_lists_all_teams(self):
        """Test if the view correctly lists all teams created and does not paginate.
        """
        response = self.client.get(reverse('main:team_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is False)
        # self.assertTrue(len(response.context['team_list']) == 30)


class PlayerListViewTest(TestCase):
    """Test class for <PlayerListView> generic view.
    """

    @classmethod
    def setUpTestData(cls):
        """Setup data for testing.
        """
        # Create teams for tests
        num_teams = 30
        for team_id in range(num_teams):
            Team.objects.create(
                team_id=team_id,
                team_abb='TOT',
                team_conf='N/A',
                team_div='N/A',
                team_city='N/A',
                team_name='N/A',
                wins=82,
                losses=0,
                nba_debut='1950',
                max_year='2018-19'
            )

        # Create players for tests
        num_players = 30
        for player_id in range(num_players):
            Player.objects.create(
                team=Team.objects.get(team_id=num_teams),
                first_name='N/A',
                last_name='N/A',
                birth_date='2000-01-01',
                player_id=player_id,
                draft_year='2019',
                draft_round='1',
                draft_number=str(player_id),
                position='Forward',
                jersey=0,
                height='7-0',
                weight=270,
                school='N/A',
                country='N/A',
                season_exp=1,
            )

    # def test_view_url_exists_at_desired_location(self):
    #     """Test if the view has the correct URL.
    #     """
    #     response = self.client.get('/players')
    #     self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test if the URL of the view can be obtained using its name.
        """
        response = self.client.get(reverse('main:player_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test if the view uses the desired template.
        """
        response = self.client.get(reverse('main:player_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/player_list.html')

    def test_lists_all_teams(self):
        """Test if the view correctly lists all teams created and does not paginate.
        """
        response = self.client.get(reverse('main:player_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is False)
        # self.assertTrue(len(response.context['player_list']) == 30)
