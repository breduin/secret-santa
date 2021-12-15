from django.contrib import admin
from .models import Game, Pair


admin.site.register(Pair)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'created_by',
                    'created_at',
                    'registration_deadline',
                    'gift_sending_deadline',
                    ]

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)