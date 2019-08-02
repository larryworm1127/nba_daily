"""Main App Views Module

@date: 06/02/2019
@author: Larry Shi
"""

from datetime import datetime, timedelta

from dateutil import parser
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_protect

from .forms import DateForm
from .models import Player, Team, Game, PlayerSeasonStats, PlayerTotalStats


# ==============================================================================
# Scores views
# ==============================================================================
def index(request):
    """Index page (with daily game scores).
    """
    date = datetime.today().date()
    return render_score_page(request, 'main/index.html', date, 'Home')


def score(request, date: str):
    """Scores page.
    """
    date_obj = parser.parse(date).date()
    return render_score_page(request, 'main/score.html', date_obj, date)


@csrf_protect
def render_score_page(request, page: str, date: datetime.date, title: str):
    """Render generic score page.
    """
    games = Game.objects.filter(game_date=date.strftime("%b %d, %Y"))

    # Validate date input
    if request.method == 'POST':
        form = DateForm(request.POST)
        date_input = parser.parse(form.data.get('date')).date()

        if form.is_valid():
            return redirect('main:score', date=date_input.strftime("%m-%d-%Y"))

    context = {
        'title': title,
        'date': date.strftime("%b %d, %Y"),
        'games': games,
        'closest_date': Game.get_closest_game_date(date).strftime("%m-%d-%Y")
    }
    return render(request, page, context)


# ==============================================================================
# Players views
# ==============================================================================
def players(request, player_id: str):
    """Individual player stats page.
    """
    try:
        player = Player.objects.get(player_id=player_id)
        reg_season = PlayerSeasonStats.objects.filter(player__player_id=player_id, season_type='Regular')
        post_season = PlayerSeasonStats.objects.filter(player__player_id=player_id, season_type='Post')
        reg_total = PlayerTotalStats.objects.get(player__player_id=player_id, season_type='Regular')
        post_total = PlayerTotalStats.objects.filter(player__player_id=player_id, season_type='Post').first()
    except Player.DoesNotExist:
        return redirect('main:player_list')

    context = {
        'title': player.get_full_name(),
        'player': player,
        'data': [(reg_season, reg_total), (post_season, post_total)],
    }
    return render(request, 'main/players.html', context)


class PlayerGamesDetailView(generic.DetailView):
    """Individual player season game log page.
    """
    model = Player
    slug_field = 'player_id'
    slug_url_kwarg = 'player_id'
    template_name = 'main/player_games.html'


class PlayerListView(generic.ListView):
    """Player list page.
    """
    model = Player
    queryset = Player.objects.order_by('first_name')


# ==============================================================================
# Teams views
# ==============================================================================
class TeamDetailView(generic.DetailView):
    """Individual team detail page.
    """
    model = Team
    slug_field = 'team_id'
    slug_url_kwarg = 'team_id'


class TeamGamesDetailView(generic.DetailView):
    """Individual team season game log page.
    """
    model = Team
    slug_field = 'team_id'
    slug_url_kwarg = 'team_id'
    template_name = 'main/team_games.html'


class TeamListView(generic.ListView):
    """Team list page.
    """
    model = Team
    queryset = Team.objects.filter(~Q(team_id=0))


# ==============================================================================
# Games views
# ==============================================================================
class GameDetailView(generic.DetailView):
    """Single game box score page.
    """
    model = Game
    slug_field = 'game_id'
    slug_url_kwarg = 'game_id'

    def get_context_data(self, **kwargs):
        """Return the updated context data.
        """
        context = super(GameDetailView, self).get_context_data(**kwargs)
        game = get_object_or_404(Game, game_id=self.kwargs['game_id'])
        context['overtime'] = range(1, game.overtime() + 1)
        return context


# ==============================================================================
# Standing views
# ==============================================================================
def standing(request):
    """Season standing page.
    """
    context = {
        'title': 'Standing',
        'headers': [('bg-danger', 'East Conference'), ('bg-primary', 'West Conference')],
    }
    return render(request, 'main/standing.html', context)
