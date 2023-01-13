from django.shortcuts import render
from .models import Game

def index(request):
    """ View function for index page """
    return render(request, 'index.html')



def game(request):
    return render(request, 'game.html')


def game_room(request, pk):
    """ View for game_room web page """
    game = Game.objects.get(id=pk)
    context = {
        'game_owner' : game.owner,
        'game_opponent' : game.opponent,
        'pk' : pk,
        'game_end_status' : game.game_end_status,
    }
    return render(request, 'game_room.html', context=context)


def waiting_opponent_view(request, pk):
    """ View for waiting opponent web page """
    game = Game.objects.get(id=pk)
    return render(request, 'waiting_opponent.html')