from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import Game


class GameCreateForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = timezone.now()
        tomorrow = today + timedelta(days=1)
        self.fields['registration_deadline'].initial = tomorrow.strftime('%Y-%m-%d')
        self.fields['gift_sending_deadline'].initial = tomorrow.strftime('%Y-%m-%d')

    class Meta:
        model = Game
        fields = [
            'name',
            'description',
            'gift_cost_limit',
            'registration_deadline',
            'gift_sending_deadline',
            'is_creator_participant',
            'place',       
            ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'название'
                    }
                    ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    }
                    ),
            'place': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Оставьте поле пустым, если игра проводится через email-рассылку'
                    }
                    ),                               
            'gift_cost_limit': forms.Select(
                attrs={
                    'class': 'form-control',
                    }
                    ),                    
            'registration_deadline': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    }
                    ),
            'gift_sending_deadline': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    }
                    ),    
        }


class GameUpdateForm(GameCreateForm):

    class Meta(GameCreateForm.Meta):
        fields = GameCreateForm.Meta.fields + [
            'administrators',
            'participants',
            ]
