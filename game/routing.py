from django.urls import path
from .consumers import IndexConsumer, GameRoomConsumer, WaitingOpponentConsumer

ws_urlpatterns = [
    path('ws/index/', IndexConsumer.as_asgi()),
    path('ws/index/game/<int:pk>/', GameRoomConsumer.as_asgi()),
     path('ws/index/game/waiting/<int:pk>/', WaitingOpponentConsumer.as_asgi()),
    ]
