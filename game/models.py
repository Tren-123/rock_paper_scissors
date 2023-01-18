from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class User(AbstractUser):
    """ Now it is not using, but can be usefull in case of custom user model needs """
    pass


class UserProfile(models.Model):
    """ Model representing a blogger info """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True, help_text="Enter your date of birth")
    games_played = models.PositiveIntegerField(default=0)
    games_won = models.PositiveIntegerField(default=0)
    short_bio = models.TextField(max_length=1000, blank=True, null=True, help_text="Enter your short bio")

    def __str__(self):
        """ String for representing the Model object. """
        return f'{self.user.username}_profile'
    
    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'user_id' : self.user_id})


class Game(models.Model):
    """ Model to represent game condition """
    game_name = models.CharField(max_length=20, default='game')
    owner = models.ForeignKey(User, related_name= 'owner', null=True, on_delete=models.SET_NULL)
    opponent  = models.ForeignKey(User, related_name= 'opponent', null=True, blank=True, on_delete=models.SET_NULL)
    game_end_status = models.BooleanField(default=False)
    winner = models.ForeignKey(User, related_name= 'winner', null=True, on_delete=models.SET_NULL)
    date_of_the_game = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        """ String for representing the Model object. """
        return f"{self.game_name}"