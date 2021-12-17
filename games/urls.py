"""Games app URL Configuration."""
from django.urls import path
from .views import MainPageView
from .views import CreateGameView
from .views import UpdateGameView
from .views import get_error_page


urlpatterns = [
    path('', MainPageView.as_view(), name='main_page'),
    path('create-game/', CreateGameView.as_view(), name='create_game'),
    path('update-game/<int:pk>', UpdateGameView.as_view(), name='update_game'),
    path('error/<int:error_code>', get_error_page, name='error'),
]
