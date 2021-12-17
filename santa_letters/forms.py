from django import forms

from .models import LetterToSanta


class LetterToSantaForm(forms.ModelForm):
    
    class Meta:
        model = LetterToSanta
        fields = [
            'text',       
            ]
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': '3',
                    }
                    ),                    
        }
