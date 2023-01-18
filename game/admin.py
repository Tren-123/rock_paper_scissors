from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Game, UserProfile

admin.site.register(User, UserAdmin)
admin.site.register(Game)
admin.site.register(UserProfile)