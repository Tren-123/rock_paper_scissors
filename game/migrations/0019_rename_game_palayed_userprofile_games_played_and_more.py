# Generated by Django 4.1.4 on 2023-01-18 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='game_palayed',
            new_name='games_played',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='game_won',
            new_name='games_won',
        ),
    ]
