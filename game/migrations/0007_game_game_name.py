# Generated by Django 4.1.4 on 2023-01-09 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_alter_game_winner'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_name',
            field=models.CharField(default='game', max_length=20),
        ),
    ]