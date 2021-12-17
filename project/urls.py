"""Project URL Configuration."""
from django.contrib import admin
from django.urls import path, include
from . import settings

urlpatterns = [
    path('letters-to-santa/', include('santa_letters.urls')),
    path('admin/', admin.site.urls),
    path('', include('games.urls')),
    path('', include('accounts.urls')),
    path('', include('mailing.urls')),
    path('', include('user_profile.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include('debug_toolbar.urls')),
    ] + urlpatterns
