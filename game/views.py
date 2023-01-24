from django.shortcuts import render, redirect
from .models import Game, User, UserProfile
from .forms import CreateUserForm, EditUserProfileForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from collections import namedtuple


def index(request):
    """ View function for index page """
    return render(request, 'index.html')


def game(request):
    """ View for ofline game page """
    return render(request, 'game.html')


def game_room(request, pk):
    """ View for game_room page """
    game = Game.objects.get(id=pk)
    context = {
        'game_owner' : game.owner,
        'game_opponent' : game.opponent,
        'pk' : pk,
        'game_end_status' : game.game_end_status,
    }
    return render(request, 'game_room.html', context=context)


def waiting_opponent_view(request, pk):
    """ View for waiting opponent page """
    game = Game.objects.get(id=pk)
    context = {
        'game_name' : game.game_name
    }
    return render(request, 'waiting_opponent.html', context=context)


def NewUserCreate(request, *args, **kwargs):
    """ View for signin new user page """
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        new_user_username = form["username"].value()
        new_user_password1 = form["password1"].value()
        new_user_password2 = form["password2"].value()
        if form.is_valid():
            try:
                validate_password(form.cleaned_data['password1'])
                if new_user_password1 == new_user_password2:
                    user = User.objects.create_user(username=new_user_username, password=new_user_password1)
                    UserProfile.objects.create(user=user)
                    login(request, user)
                    return HttpResponseRedirect('/')
            except ValidationError as e:
                form.add_error('password1', e)
            
    else:
        form = CreateUserForm()
    return render(request, 'registration/signup.html', {'form': form})


def leader_list(request):
    """ View for game_room page """
    users_results = UserProfile.objects.all()
    list_of_users_results= []
    User_info = namedtuple('User_info', 'user_id, username, games_played, games_won')
    for user in users_results:
        list_of_users_results.append(User_info(user.user_id, str(user.user), user.games_played, user.games_won))
    sorted_list_by_games_won = sorted(list_of_users_results, key=lambda user_tupple: user_tupple.games_won, reverse=True)
    context = {
        'list_of_users_results' : sorted_list_by_games_won,
    }
    return render(request, 'leaders_list.html', context=context)


def user_profile(request, user_id):
    """ View for userprofile page """
    user = User.objects.get(id=user_id)
    userprofile = UserProfile.objects.get(user_id=user_id)
    context = {
        'username' : user.username,
        'first_name' : user.first_name,
        'last_name' : user.last_name,
        'date_of_birth' : userprofile.date_of_birth,
        'short_bio' : userprofile.short_bio,
        'games_won' : userprofile.games_won,
        'games_played' : userprofile.games_played,
        'user_id': user_id,
    }
    return render(request, 'user_profile.html', context=context)


def edit_user_profile(request, user_id):
    """ View for handle edit user profile page """
    user = User.objects.get(id=user_id)
    userprofile = UserProfile.objects.get(user_id=user_id)
    if request.user == user:
        if request.method == 'POST':
            form = EditUserProfileForm(request.POST)
            first_name = form["first_name"].value()
            last_name = form["last_name"].value()
            about_me = form["about_me"].value()
            if form.is_valid():
                user.first_name = first_name
                user.last_name = last_name
                userprofile.short_bio = about_me
                user.save()
                userprofile.save()
                return redirect(userprofile)           
        else:
            data = {'first_name': user.first_name, 'last_name': user.last_name, 'about_me': userprofile.short_bio}
            form = EditUserProfileForm(initial=data)
            context = {'form': form}
        return render(request, 'edit_user_profile.html', context)
    return redirect(userprofile)   