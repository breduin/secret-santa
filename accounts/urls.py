"""Games app URL Configuration."""
from django.urls import path
from accounts import views


urlpatterns = [
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('user-update/<int:pk>', views.UserUpdateView.as_view(), name='user_update'),
    path('password_change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password_change_done/', views.UserPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', views.UserPasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),    
]
