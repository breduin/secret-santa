from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, WishListItem


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('address', 'wishlist',)}),
    )


admin.site.register(User, CustomUserAdmin)

admin.site.register(WishListItem)