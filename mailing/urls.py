"""Games app URL Configuration."""
from django.urls import path
from mailing import views


urlpatterns = [
    path('mailing/<int:game_id>/', views.mass_mailing, name='mass_mailing'),
    path('mailing/<int:game_id>/<int:user_id>/', views.pair_mailing, name='pair_mailing'),
]
