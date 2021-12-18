# Generated by Django 4.0 on 2021-12-18 07:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0006_alter_game_description_alter_game_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_online',
            field=models.BooleanField(default=True, verbose_name='Игра проводится онлайн?'),
        ),
        migrations.AddField(
            model_name='game',
            name='your_gift_cost_limit',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Ваш лимит стоимости подарка'),
        ),
        migrations.AlterField(
            model_name='game',
            name='gift_cost_limit',
            field=models.CharField(choices=[('UPTO500', 'до 500 рублей'), ('500_1000', '500-1000 рублей'), ('1000_2000', '1000-2000 рублей'), ('YOUR', 'задать свой лимит')], default='UPTO500', max_length=50, verbose_name='Стоимость подарка'),
        ),
        migrations.AlterField(
            model_name='game',
            name='place',
            field=models.CharField(blank=True, max_length=256, verbose_name='Место встречи'),
        ),
    ]
