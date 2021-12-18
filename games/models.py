from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models



class Game(models.Model):
    """Игра."""
    COST_LIMIT_CHOICES = (    
    ('UPTO500', 'до 500 рублей'),
    ('500_1000', '500-1000 рублей'),
    ('1000_2000', '1000-2000 рублей'),
    ('YOUR', 'задать свой лимит'),
    )

    name = models.CharField(
        verbose_name='Название', 
        max_length=256,
        help_text='Укажите название игры'
        )
    description = models.TextField(
        verbose_name='Описание', 
        max_length=256,
        blank=True,
        )
    place = models.CharField(
        verbose_name='Место встречи', 
        max_length=256,
        blank=True,      
        )        
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
        db_index=True,
        )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name='Время редактирования',
        )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='created_games',
        editable=False,
        )
    gift_cost_limit = models.CharField(
        verbose_name='Стоимость подарка', 
        max_length=50,
        choices=COST_LIMIT_CHOICES,
        default='UPTO500',
        )    
    your_gift_cost_limit = models.PositiveIntegerField(
        verbose_name='Ваш лимит стоимости подарка', 
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
        )      
    registration_deadline = models.DateField(
        verbose_name='Дата окончания регистрации',
        )
    gift_sending_deadline = models.DateField(
        verbose_name='Отправить подарок до',
        )        
    administrators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='managed_games',
        blank=True,
        )        
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='games',
        blank=True,
        )
    is_participants_shuffled = models.BooleanField(default=False,
                                                   verbose_name='Участники перемешаны')

    is_creator_participant = models.BooleanField(
        default=True,
        verbose_name='Буду участником?',
        )
    is_online = models.BooleanField(
        default=True,
        verbose_name='Игра проводится онлайн?',
        )    

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class Pair(models.Model):
    """Пара игроков, полученная в результате жеребьёвки."""
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
        )    
    giver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='givers',
        db_index=True,
        )    
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipients',
        db_index=True,
        ) 
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='pairs',
        )        
    is_gift_sent = models.BooleanField(
        verbose_name="Подарок отправлен?",
        default=False,
        )

    def __str__(self):
        return f'Пара №{self.id} к игре {self.game}'

    class Meta:
        verbose_name = 'Пара'
        verbose_name_plural = 'Пары'
