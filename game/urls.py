from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= "index"),
    path('game/', views.game, name= "game"),
    path('game_online/', views.game_online, name= "game_online"),
    path('game/<int:pk>/', views.game_room, name="game_room")
    ]