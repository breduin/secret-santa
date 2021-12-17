# Generated by Django 4.0 on 2021-12-17 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_game_description_game_is_creator_participant'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='place',
            field=models.CharField(blank=True, help_text='Оставьте поле пустым, если игра проводится через email-рассылку', max_length=256, null=True, verbose_name='Место встречи'),
        ),
        migrations.AlterField(
            model_name='game',
            name='is_creator_participant',
            field=models.BooleanField(default=True, verbose_name='Буду участником?'),
        ),
    ]
