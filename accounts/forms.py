from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordResetForm
from django.utils.html import format_html
from .models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'username',
                                      }
                               ),
    )
    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'class': 'form-control',
                                          'placeholder': 'password',
                                          }
                                   ),
    )


class GameUserCreateForm(UserCreationForm):
    required_css_class = 'fw-bold'
    consent_to_processing_pd = forms.BooleanField(
        label="""Я даю согласие на обработку своих персональных данных 
                 соответствии с требованиями Федерального закона 
                 №152-ФЗ от 27.07.2006.
        """
        ) 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].label = 'Логин'

    def clean_consent_to_processing_pd(self):
        consent = self.cleaned_data.get('consent_to_processing_pd')
        if not consent:
            raise ValidationError(
                self.error_messages[
                    'Необходимо согласие на обработку персональных данных.'
                    ],
                code='invalid_value',
            )
        return consent

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('email',
                                                 'first_name',
                                                 'last_name'
                                                 )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'логин'
                    }
                    ),
            'password2': forms.PasswordInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'пароль'
                    }
                    ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'pochta@primer.ru'
                    }
                    ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Имя'
                    }
                    ),    
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Фамилия'
                    }
                    ),
            'consent_to_processing_pd': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                    }
                    ),                                                 
        }


class UserPasswordResetForm(PasswordResetForm):
    pass


class UserUpdateForm(GameUserCreateForm):
    """
    Form to update user profile data.
    """
    class Meta(GameUserCreateForm.Meta):
        fields = GameUserCreateForm.Meta.fields
