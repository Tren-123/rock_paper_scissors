from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Now it is not using, but can be usefull in case of custom user model needs """
    pass


class Game(models.Model):
    """ Model to represent game condition """
    game_name = models.CharField(max_length=20, default='game')
    owner = models.ForeignKey(User, related_name= 'owner', null=True, on_delete=models.SET_NULL)
    opponent  = models.ForeignKey(User, related_name= 'opponent', null=True, blank=True, on_delete=models.SET_NULL)
    game_end_status = models.BooleanField(default=False)
    winner = models.PositiveIntegerField(default=0)
    date_of_the_game = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        """ String for representing the Model object. """
        return f"{self.game_name}"