from django.contrib import admin
from .models import Game
from .models import Pair
from .models import WishList
from .models import ElidiblePair


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


class PairAdmin(admin.ModelAdmin):
    list_filter = ['game', 'giver']
    list_display = ['id', 'game', 'giver', 'recipient']


admin.site.register(Pair, PairAdmin)

admin.site.register(WishList)

admin.site.register(ElidiblePair)
