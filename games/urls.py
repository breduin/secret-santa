"""Games app URL Configuration."""
from django.urls import path
from .views import MainPageView, CreateGameView, UpdateGameView

urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('create-game/', CreateGameView.as_view(), name='create_game'),
    path('update-game/<int:pk>', UpdateGameView.as_view(), name='update_game'),
]
