from django.urls import path, re_path
from .consumers import ChatConsumer, GameOnlineConsumer, AsyncGameConsumer, IndexConsumer, GameRoomConsumer

ws_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    path('ws/game_online/', AsyncGameConsumer.as_asgi()),
    path('ws/index/', IndexConsumer.as_asgi()),
    path('ws/index/game/<int:pk>/', GameRoomConsumer.as_asgi()), 
    ]
