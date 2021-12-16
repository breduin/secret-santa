from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['username'].label = 'Логин'

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
        }


class UserPasswordResetForm(PasswordResetForm):
    pass
