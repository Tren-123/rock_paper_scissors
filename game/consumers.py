import json
from channels.generic.websocket import WebsocketConsumer
from .models import Game, UserProfile
from asgiref.sync import async_to_sync


class IndexConsumer(WebsocketConsumer):
    """ Consumer for user on index page """
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game = None
        self.user = None
        self.index_pg_chat_name = 'chat_index_page'


    def connect(self):
        # connect with consumer with client side
        self.user = self.scope['user']
        async_to_sync(self.channel_layer.group_add)(
            self.index_pg_chat_name,
            self.channel_name,
        )
        self.accept()


    def disconnect(self, close_code):
        # Disconnect consumer instance from client side and discard chanell name from group in chanell layer
        async_to_sync(self.channel_layer.group_discard)(
            self.index_pg_chat_name,
            self.channel_name,
        )

    
    def receive(self, text_data=None, bytes_data=None):
        # Handle message from frontend
        text_data_json = json.loads(text_data)
        # Request list of game with vacant opponent role from db and send it to frontend 
        if text_data_json['message'] == 'update':
            data = Game.objects.filter(opponent__isnull = True, game_end_status = False).order_by("date_of_the_game")
            list_of_game = []
            for i in data:
                list_of_game.append((str(i), i.id, str(i.owner)))
            self.send(json.dumps({'message' : 'update', 'user' : self.user.username, 'list_of_game' : list_of_game}))
        # Updated db - fill opponent field 
        elif text_data_json['message'] == 'opponent_connected':
            self.game = Game.objects.get(id=text_data_json['game_id'])
            self.game.opponent = self.user
            self.game.save()
            print(text_data_json['game_id'])
        # Create new instance for game in and fill owner field. Send message with new game id to frontend
        elif text_data_json['message'] == 'create_game':
            if self.user.is_authenticated:
                new_game = Game(game_name=text_data_json['game_name'], owner=self.user)
                new_game.save()
                print(new_game)
                self.send(json.dumps({'message' : 'new_game', 'id' : new_game.id}))
                print(text_data_json)
        elif text_data_json['message'] == 'send_message_to_chat':
            async_to_sync(self.channel_layer.group_send)(
            self.index_pg_chat_name,
            {
                'type': 'chat_send_message_to_chat',
                'message': 'chat_send_message_to_chat',
                'message_body': text_data_json['message_body'],
                'user': (str(self.user)),
            }
            )


    def chat_send_message_to_chat(self, event):
        # handle chat_send_message_to_chat method
        self.send(text_data=json.dumps(event))


class WaitingOpponentConsumer(WebsocketConsumer):
    """ Consumer for user - owner of the game, which waiting opponent. Working on waiting opponent web page """
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game = None
        self.user = None


    def connect(self):
        # connect with consumer with client side
        self.user = self.scope['user']
        self.game_id = self.scope['url_route']['kwargs']['pk']
        self.game = Game.objects.get(id=self.game_id)
        self.accept()


    def receive(self, text_data=None, bytes_data=None):
        # handle message from frontend
        text_data_json = json.loads(text_data)
        # Request game instancce from db and check if opponent role filled. If yes - send message to frontend 
        if text_data_json['message'] == 'update':
            data = Game.objects.get(id=self.game_id)
            if data.opponent:
                self.send(json.dumps({'message' : 'opponent_here', 'game_id' : self.game_id}))
    


class GameRoomConsumer(WebsocketConsumer):
    """ Consumer for user in game room """
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_id = None
        self.game_group_name = None
        self.game = None
        self.user = None
        self.role = None
        self.owner = None
        self.opponent = None
        self.owner_profile = None
        self.opponent_profile = None
        self.owner_opponent_games_played_and_won = None
        self.owner_weapon = None
        self.opponent_weapon = None


    def connect(self):
        # connect with consumer with client side. Check role and set instance parameters. Added new consumer instance in group in chanell layer
        self.user = self.scope['user']
        self.game_id = self.scope['url_route']['kwargs']['pk']
        self.game = Game.objects.get(id=self.game_id)
        self.game_group_name = f'game_{self.game_id}'
        self.owner_profile = UserProfile.objects.get(user_id=self.game.owner_id)
        self.opponent_profile = UserProfile.objects.get(user_id=self.game.opponent_id)
        self.owner_opponent_games_played_and_won = {
                'owner' : [self.owner_profile.games_played, self.owner_profile.games_won],
                'opponent' : [self.opponent_profile.games_played, self.opponent_profile.games_won],
                }
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
        else:
            self.close()
            

    def disconnect(self, close_code):
        # Disconnect consumer instance from client side and discard chanell name from group in chanell layer
        print(f'connection closed, CLOSE CODE: {close_code}')
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name,
        )
    

    def receive(self, text_data=None, bytes_data=None):
        # handle message from frontend
        text_data_json = json.loads(text_data)
        # get owner/opponent weapon choise from frontend and send message to group in chanell layer
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
        elif text_data_json['message'] == 'send_message_to_room_chat':
            async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': 'chat_send_message_to_room_chat',
                'message': 'chat_send_message_to_room_chat',
                'message_body': text_data_json['message_body'],
                'user': (str(self.user)),
            }
            )


    def game_referee(self):
        # decide game result, send it to group on frontend and set it to db if winner determined
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
            self.owner_profile.games_played = self.owner_opponent_games_played_and_won['owner'][0] + 1
            self.opponent_profile.games_played = self.owner_opponent_games_played_and_won['opponent'][0] + 1
            if winner == self.owner[0]:
                self.game.winner = self.game.owner
                self.owner_profile.games_won = self.owner_opponent_games_played_and_won['owner'][1] + 1
            elif winner == self.opponent[0]:
                self.game.winner = self.game.opponent
                self.opponent_profile.games_won = self.owner_opponent_games_played_and_won['opponent'][1] + 1
            self.game.save()
            self.owner_profile.save()
            self.opponent_profile.save()
        self.owner_weapon, self.opponent_weapon = None, None

    def owner_weapon_choosed(self, event):
        # handle owner_weapon_choosed event. If called inside owner consumer and opponent have already choose weapon - call  game_referee method to decided game
        self.owner_weapon = event['owner_weapon']
        self.owner = event['owner']
        if self.role == 'owner' and self.opponent_weapon != None:
            self.game_referee()


    def opponent_weapon_choosed(self, event):
        # handle opponent_weapon_choosed event. If called inside owner consumer and owner have already choose weapon - call  game_referee method to decided game
        self.opponent_weapon = event['opponent_weapon']
        self.opponent = event['opponent']
        if self.role == 'owner' and self.owner_weapon != None:
            self.game_referee()


    def send_result(self, event):
        # handle send_result method from game_referee method
        self.send(text_data=json.dumps(event))


    def chat_send_message_to_room_chat(self, event):
        # handle chat_send_message_to_room_chat method
        self.send(text_data=json.dumps(event))


