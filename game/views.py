from django.shortcuts import render

def index(request):
    """ View function for index page """

    context = {
        'text' : 'Game here'
    }
    return render(request, 'index.html', context=context)


def chat_index(request):
    return render(request, 'chat_index.html')

def room(request, room_name):
    return render(request, "room.html", {"room_name": room_name})

def game(request):
    return render(request, 'game.html')