"""Games app URL Configuration."""
from django.urls import path
from user_profile import views


urlpatterns = [
    path('profile/<int:profile_id>/', views.profile, name='profile'),
    path('toss/<int:game_id>/', views.game_toss, name='toss'),
]
