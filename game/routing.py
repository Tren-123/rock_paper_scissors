from django.urls import path, re_path
from .consumers import GameConsumer, ChatConsumer

ws_urlpatterns = [
    path('ws/game/', GameConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    ]
