from datetime import timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

from accounts.models import User
from .models import Game
from .models import WishList
from .models import ElidiblePair


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
            'your_gift_cost_limit',
            'registration_deadline',
            'gift_sending_deadline',
            'is_creator_participant',
            'is_online',
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
                    }
                    ),
            'gift_cost_limit': forms.Select(
                attrs={
                    'class': 'form-control',
                    }
                    ),
            'your_gift_cost_limit': forms.NumberInput(
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
            'is_creator_participant': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    }
                    ),
            'is_online': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    'role': 'switch',
                    }
                    ),
        }


class GameUpdateForm(GameCreateForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['participants'].queryset = User.objects.all().order_by('username')
        self.fields['administrators'].queryset = User.objects.all().order_by('username')

    class Meta(GameCreateForm.Meta):
        fields = GameCreateForm.Meta.fields + [
            'administrators',
            'participants',
            ]
        widgets = GameCreateForm.Meta.widgets.copy()
        widgets.update({
            'participants': forms.SelectMultiple(
                attrs={
                    'size': 5,
                    'class': 'form-select',
                    }
                    ),
            'administrators': forms.SelectMultiple(
                attrs={
                    'size': 5,
                    'class': 'form-select',
                    }
                    ),                       
        })

class WishListCreateForm(forms.ModelForm):

    class Meta:
        model = WishList
        fields = [
            'items',
            ]
        widgets = {
            'items': forms.SelectMultiple(
                attrs={
                    'size': 15,
                    'class': 'form-select',
                    }
                    ),              
        }

class ElidiblePairCreateForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        game_id = kwargs.pop('game_id')
        super().__init__(*args, **kwargs)
        self.fields['user_1'].queryset = User.objects.filter(
            games__id=game_id
            ).order_by('username')
        self.fields['user_2'].queryset = User.objects.filter(
            games__id=game_id
            ).order_by('username')

    def clean_user_2(self):
        user_2 = self.cleaned_data.get('user_2')
        user_1 = self.cleaned_data.get('user_1')
        if user_2 == user_1:
            raise ValidationError('В паре-исключении должны быть разные люди.')
        return user_2

    class Meta:
        model = ElidiblePair
        fields = [
            'user_1',
            'user_2',            
            ]
        widgets = {
            'user_1': forms.Select(
                attrs={
                    'class': 'form-select',
                    }
                    ),
            'user_2': forms.Select(
                attrs={
                    'class': 'form-select',
                    }
                    ),
        }
