from django.contrib.auth.models import AbstractUser
from django.db import models


class WishListItem(models.Model):
    """ Элемент списка пожеланий"""
    name = models.CharField('Название', 
                            max_length=256,
                            help_text='Укажите пожелание'
                            )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Элемент списка пожеланий'
        verbose_name_plural = 'Элементы списка пожеланий'


class User(AbstractUser):
    """Пользователь."""
    address = models.CharField('Почтовый адрес', 
                                max_length=512, 
                                blank=True,
                                )
    def __str__(self):
        if (fname := self.first_name) and (lname := self.last_name):
            return '{} {} ({})'.format(fname, lname, self.username)
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


