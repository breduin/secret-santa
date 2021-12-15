from django.conf import settings
from django.db import models


class LetterToSanta(models.Model):
    """Письмо Санте."""
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время создания',
        db_index=True,
        )    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='letters_to_santa',
        editable=False,
        )
    text = models.TextField(
        verbose_name='Текст письма',
        )        

    def __str__(self):
        return f'Письмо Санте от {self.created_by}'

    class Meta:
        verbose_name = 'Письмо Санте'
        verbose_name_plural = 'Письма Санте'
        