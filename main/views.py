from django.shortcuts import render


def index(request):
    """Index page.
    """
    context = {
        'title': "Home"
    }
    return render(request, 'main/index.html', context)


def players(request):
    """Individual player stats page.
    """
    context = {
        'title': "Player",
        'player_summary_info': []
    }
    return render(request, 'main/players.html', context)
