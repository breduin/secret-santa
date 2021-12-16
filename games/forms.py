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
            'gift_cost_limit',
            'registration_deadline',
            'gift_sending_deadline',            
            ]
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'название'
                    }
                    ),
            'gift_cost_limit': forms.Select(
                attrs={
                    'class': 'form-control',
                    }
                    ),                    
            'registration_deadline': forms.DateInput(
                format='%d-%m-%Y',
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                    }
                    ),
            'gift_sending_deadline': forms.DateInput(
                format='%d-%m-%Y',
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
