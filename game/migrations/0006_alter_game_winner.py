# Generated by Django 4.1.4 on 2023-01-09 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_alter_game_game_end_status_alter_game_participant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.PositiveIntegerField(default=0),
        ),
    ]