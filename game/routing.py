from django.urls import path, re_path
from .consumers import IndexConsumer, GameRoomConsumer

ws_urlpatterns = [
    path('ws/index/', IndexConsumer.as_asgi()),
    path('ws/index/game/<int:pk>/', GameRoomConsumer.as_asgi()), 
    ]
