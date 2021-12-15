"""Games app URL Configuration."""
from django.urls import path
from accounts import views


urlpatterns = [
    path('profile/<int:profile_id>/', views.profile),
]
