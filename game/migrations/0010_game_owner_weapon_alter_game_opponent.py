# Generated by Django 4.1.4 on 2023-01-11 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_alter_game_opponent'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='owner_weapon',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='opponent',
            field=models.CharField(max_length=20, null=True),
        ),
    ]