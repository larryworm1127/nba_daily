"""Main App View Test Module

@date: 07/27/2019
@author: Larry Shi
"""
from unittest import skip

from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from main.models import Team, Player


@skip
class TeamListViewTest(SimpleTestCase):
    """Test class for <TeamListView> generic view.
    """

    def test_view_url_exists_at_desired_location(self):
        """Test if the view has the correct URL.
        """
        response = self.client.get('/teams/')
        self.assertEqual(response.status_code, 200)

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
        self.assertTemplateUsed(response, 'main/teams_stats.html')


@skip
class PlayerListViewTest(TestCase):
    """Test class for <PlayerListView> generic view.
    """

    @classmethod
    def setUpTestData(cls):
        """Setup data for testing.
        """
        # Create teams/players for tests
        num_teams = 30
        for team_id in range(num_teams):
            team = Team.objects.create(
                team_id=team_id,
                team_abb='TOT',
                team_conf='N/A',
                team_div='N/A',
                team_city='N/A',
                team_name='N/A',
                nba_debut='1950',
                max_year='2018-19'
            )

            Player.objects.create(
                team=team,
                first_name='N/A',
                last_name='N/A',
                birth_date='2000-01-01',
                player_id=team_id,
                draft_year='2019',
                draft_round='1',
                draft_number=str(team_id),
                position='Forward',
                jersey=0,
                height='7-0',
                weight=270,
                school='N/A',
                country='N/A',
                season_exp=1,
            )

    def test_view_url_exists_at_desired_location(self):
        """Test if the view has the correct URL.
        """
        response = self.client.get('/players/')
        self.assertEqual(response.status_code, 200)

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
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['player_list']) == 20)
