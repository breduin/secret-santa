from django.shortcuts import get_object_or_404, render
from accounts.models import User


def serialize_users(users):
    user_names = [f'{user.first_name} {user.last_name}' for user in users]
    return ', '.join(user_names)


def serialize_game(game, user):
    return {
        'name': game.name,
        'is_admin': user in game.administrators.all(),
        'admins': serialize_users(game.administrators.all()),
        'participants_count': game.participants.count(),
        'id': game.id,
        'created_at': game.created_at,
        'gift_cost_limit': game.get_gift_cost_limit_display(),
        'registration_deadline': game.registration_deadline,
        'gift_sending_deadline': game.gift_sending_deadline,
        'participants': serialize_users(game.participants.all()),
    }
         

def profile(request, profile_id):
    user = get_object_or_404(
        (
            User.objects
            .prefetch_related('games__administrators')
            .prefetch_related('games__participants')
        ),
        id=profile_id
    )
    
    games = user.games.all()
    context = {
        'user': user,
        'games': [serialize_game(game, user) for game in games],
    }

    return render(request, 'profile.html', context)
