from django.shortcuts import get_object_or_404, render
from accounts.models import User


def serialize_game(game, user):
    administrators = [f'{administrator.first_name} {administrator.last_name}'
                      for administrator in game.administrators.all()]
    return {
        'name': game.name,
        'is_admin': user in game.administrators.all(),
        'admins': ', '.join(administrators),
        'participants_count': game.participants.count(),
        'id': game.id,
    }


def profile(request, profile_id):
    user = get_object_or_404(
        User.objects.prefetch_related('games__administrators'),
        id=profile_id
    )
    
    games = user.games.all()
    context = {
        'user': user,
        'games': [serialize_game(game, user) for game in games],
    }

    return render(request, 'profile.html', context)
