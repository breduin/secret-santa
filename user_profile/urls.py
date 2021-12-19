"""Games app URL Configuration."""
from django.urls import path
from user_profile import views
from games.views import ElidiblePairCreateView


urlpatterns = [
    path('profile/<int:profile_id>/', views.profile, name='profile'),
    path('toss/<int:game_id>/', views.game_toss, name='toss'),
    path('create_elidible_pair/<int:game_id>/', ElidiblePairCreateView.as_view(), name='create_elidible_pair'),
]
