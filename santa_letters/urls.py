"""Letter to Santa app URL Configuration."""
from django.urls import path
from .views import LetterToSantaCreateView

urlpatterns = [
    path(
        'write/user/<int:pk>',
        LetterToSantaCreateView.as_view(),
        name='write_letter_to_santa'),
]