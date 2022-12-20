from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ Now it is not using, but can be usefull in case of custom user model needs """
    pass
