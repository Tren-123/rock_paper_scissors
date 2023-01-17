from django.shortcuts import render
from .models import Game, User
from .forms import CreateUserForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

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
    context = {
        'game_name' : game.game_name
    }
    return render(request, 'waiting_opponent.html', context=context)


def NewUserCreate(request, *args, **kwargs):
    """ View for signin new user web page """
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        new_user_username = form["username"].value()
        new_user_password1 = form["password1"].value()
        new_user_password2 = form["password2"].value()
        if form.is_valid():
            print(form.cleaned_data)
            try:
                validate_password(form.cleaned_data['password1'])
                if new_user_password1 == new_user_password2:
                    user = User.objects.create_user(username=new_user_username, password=new_user_password1)
                    login(request, user)
                    return HttpResponseRedirect('/')
            except ValidationError as e:
                form.add_error('password1', e)
            
    else:
        form = CreateUserForm()
    return render(request, 'registration/signin.html', {'form': form})