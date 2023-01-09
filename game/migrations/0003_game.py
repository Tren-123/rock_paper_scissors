# Generated by Django 4.1.4 on 2023-01-09 07:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_test_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_end_status', models.BooleanField()),
                ('winner', models.PositiveIntegerField()),
                ('date_of_the_game', models.DateTimeField(auto_now_add=True)),
                ('game_owner', models.ManyToManyField(related_name='owner', to=settings.AUTH_USER_MODEL)),
                ('game_participant', models.ManyToManyField(related_name='participant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
