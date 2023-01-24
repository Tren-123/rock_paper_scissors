from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= "index"),
    path('game/', views.game, name= "game"),
    path('game/<int:pk>/', views.game_room, name="game_room"),
    path('game/waiting/<int:pk>/', views.waiting_opponent_view, name="waiting_opponent"),
    path('userprofile/<int:user_id>/', views.user_profile, name="user_profile"),
    path('leaders/', views.leader_list, name="leader_list"),
    path('userprofile/<int:user_id>/edit/', views.edit_user_profile, name='edit_user_profile')
    ]