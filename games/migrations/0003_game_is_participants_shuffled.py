# Generated by Django 4.0 on 2021-12-16 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_alter_game_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_participants_shuffled',
            field=models.BooleanField(default=False, verbose_name='Участники перемешаны'),
        ),
    ]
