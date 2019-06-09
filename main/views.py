from django.shortcuts import render


def index(request):
    context = {
        'title': "Home"
    }
    return render(request, 'main/index.html', context)


def players(request):
    context = {
        'title': "Player",
        'player_summary_info': []
    }
    return render(request, 'main/players.html', context)
