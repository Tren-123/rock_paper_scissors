from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= "index"),
    path('game/', views.game, name= "game"),
    path('game/<int:pk>/', views.game_room, name="game_room"),
    path('game/waiting/<int:pk>/', views.waiting_opponent_view, name="waiting_opponent"),
    path('signin/', views.NewUserCreate, name='user_signin'),
    ]