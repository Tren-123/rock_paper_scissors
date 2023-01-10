import json
from random import randint
from asyncio import sleep, gather
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import time
from .models import Test_model, Game
from channels.auth import get_user
from asgiref.sync import async_to_sync


class IndexConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.game = None
        self.user = None
    def connect(self):
        self.user = self.scope['user']
        self.accept()
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        if text_data_json['message'] == 'update':
            data = Game.objects.filter(opponent__isnull = True, game_end_status = False).order_by("date_of_the_game")
            list_of_game = []
            for i in data:
                list_of_game.append((str(i), i.id))
            self.send(json.dumps({'message' : 'update', 'list_of_game' : list_of_game}))
        elif text_data_json['message'] == 'opponent_connected':
            self.game = Game.objects.get(id=text_data_json['game_id'])
            self.game.opponent = self.user
            self.game.save()
            print(text_data_json['game_id'])
        elif text_data_json['message'] == 'create_game':
            new_game = Game(game_name=text_data_json['game_name'], owner=self.user)
            new_game.save()
            print(new_game)
            self.send(json.dumps({'message' : 'new_game', 'id' : new_game.id}))
            print(text_data_json)


class GameRoomConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_id = None
        self.game_group_name = None
        self.game = None
        self.user = None
        self.role = None
    def connect(self):
        self.user = self.scope['user']
        self.game_id = self.scope['url_route']['kwargs']['pk']
        self.game = Game.objects.get(id=self.game_id)
        self.game_group_name = f'game_{self.game_id}'
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name,
        )
        if self.user == self.game.owner:
            print(f'i am onwer - { self.game.owner}')
            self.accept()
            self.role = 'owner'
        elif self.user == self.game.opponent:
            print(f'i am opponent - { self.game.opponent}')
            self.accept()
            self.role = 'opponent'


    def disconnect(self, close_code):
        print(f'connection forbiden or lost, close code {close_code}')
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name,
        )
    
    def receive(self, text_data=None, bytes_data=None):
        pass

class GameOnlineConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print(f'chanel name - {self.channel_name}')
    def receive(self, text_data):
        if text_data == 'You win!':
            to_db = Test_model(game_result = 'Win')
            print('User win')
        elif text_data == 'You lose!':
             print('User lose')
             to_db = Test_model(game_result ='Lose')
        else:
            to_db = Test_model(game_result ='Draw')
            print(text_data)
        to_db.save()



class AsyncGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "game_test"
        print(self.scope['user'], self.scope['session'])
        # Join game group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        if text_data_json["user_join"]:
            print('User join!!!')
        else:
            message = text_data_json["message"]
            # Send message to room group
            await self.channel_layer.group_send(
                self.group_name, {"type": "chat_message", "message": message, "user": str(self.scope['user'])}
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        print(event)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))