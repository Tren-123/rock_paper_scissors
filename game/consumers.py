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
        self.owner = None
        self.opponent = None
        self.owner_weapon = None
        self.opponent_weapon = None

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
            async_to_sync(self.channel_layer.group_send)( #DONT WORK AS EXSPECTED NEED TO FIX (not send message after opponent connected sometime)
                self.game_group_name,
                {
                    'type': 'opponent_join_1',
                    'user': self.user.username,
                }
            )
            

    def disconnect(self, close_code):
        print(f'connection forbiden or lost, close code {close_code}')
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name,
        )
    
    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        if text_data_json['message'] == 'weapon_choose':
            if self.role == 'owner':
                self.owner_weapon = text_data_json['weapon'][0].lower()
                async_to_sync(self.channel_layer.group_send)(
                self.game_group_name,
                {
                    'type': 'owner_weapon_choosed',
                    'owner': (self.user.username, self.user.id),
                    'owner_weapon': f'{self.owner_weapon}',
                }
            )

            elif self.role == 'opponent':
                self.opponent_weapon = text_data_json['weapon'][0].lower()
                async_to_sync(self.channel_layer.group_send)(
                self.game_group_name,
                {
                    'type': 'opponent_weapon_choosed',
                    'opponent': (self.user.username, self.user.id),
                    'opponent_weapon': f'{self.opponent_weapon}',
                }
            )
    

    def game_referee(self): #DONT WORK AS EXSPECTED NEED TO FIX (not save opponent in db sometimes)
        referee_dict = { 
            'r' : ['s', 'p', 'r'],
            'p' : ['r', 's', 'p'],
            's' : ['p', 'r', 's']
        }
        winner = None
        if self.opponent_weapon == referee_dict[self.owner_weapon][0]:
            winner = self.owner[0]
        elif self.opponent_weapon == referee_dict[self.owner_weapon][1]:
            winner = self.opponent[0]
        elif self.opponent_weapon == referee_dict[self.owner_weapon][2]:
            winner = False
        print(winner)
        
        async_to_sync(self.channel_layer.group_send)(
                self.game_group_name,
                {
                    'type': 'send_result',
                    'owner': self.owner,
                    'opponent': self.opponent,
                    'winner': winner,
                    'owner_weapon': self.owner_weapon,
                    'opponent_weapon': self.opponent_weapon,
                }
            )
        if winner:
            self.game.game_end_status = True
            if winner == self.owner[0]:
                self.game.winner = self.owner[1]
            elif winner == self.opponent[0]:
                self.game.winner = self.opponent[1]
            self.game.save()
        self.owner_weapon, self.opponent_weapon = None, None

    def owner_weapon_choosed(self, event):
        self.owner_weapon = event['owner_weapon']
        self.owner = event['owner']
        if self.role == 'owner' and self.opponent_weapon != None:
            self.game_referee()


    def opponent_weapon_choosed(self, event):
        self.opponent_weapon = event['opponent_weapon']
        self.opponent = event['opponent']
        if self.role == 'owner' and self.owner_weapon != None:
            self.game_referee()

    def send_result(self, event):
        self.send(text_data=json.dumps(event))


    def opponent_join_1(self, event):
        self.send(text_data=json.dumps(event))


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


