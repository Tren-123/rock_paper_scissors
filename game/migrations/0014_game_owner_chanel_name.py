# Generated by Django 4.1.4 on 2023-01-13 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_remove_game_opponent_weapon_remove_game_owner_weapon'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='owner_chanel_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
