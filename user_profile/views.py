import datetime
from django.shortcuts import get_object_or_404, render
from games.models import Pair
from randomizer.randomizer import shuffle_game_participants
from accounts.models import User
from django.http import HttpResponse
from games.models import Game
from django.db.models import Q


def serialize_users(users):
    user_names = [f'{user.first_name} {user.last_name}' for user in users]
    return ', '.join(user_names)


def serialize_game(game, user):
    if game.pairs.filter(giver=user).exists():
        recipient = game.pairs.get(giver=user).recipient
        recipient_name = (f'{recipient.first_name} {recipient.last_name} '
                          f'({recipient.username})')
    else:
        recipient_name = None

    return {
        'name': game.name,
        'is_creator': user == game.created_by,
        'is_admin': user in game.administrators.all(),
        'is_participant': user in game.participants.all(),
        'admins': serialize_users(game.administrators.all()),
        'participants_count': game.participants.count(),
        'id': game.id,
        'created_at': game.created_at,
        'gift_cost_limit': game.get_gift_cost_limit_display(),
        'registration_deadline': game.registration_deadline,
        'gift_sending_deadline': game.gift_sending_deadline,
        'participants': serialize_users(game.participants.all()),
        'is_shuffled': game.is_participants_shuffled,
        'recipient': recipient_name,
        'description': game.description,
        'place': game.place,
        'is_online': game.is_online,
    }
         

def profile(request, profile_id):
    user = get_object_or_404(User, id=profile_id)
    host_addr = request._current_scheme_host
    user_games = (
        Game.objects
        .filter(Q(created_by=user) | Q(administrators=user) | Q(participants=user))
        .distinct()
        .prefetch_related('participants')  
        .prefetch_related('administrators') 
        .select_related('created_by')
    )
    last_games = (
        user_games
        .filter(gift_sending_deadline__lt=datetime.date.today())
        .order_by('-gift_sending_deadline')
    )
    current_games = (
        user_games
        .filter(gift_sending_deadline__gte=datetime.date.today())
        .order_by('-gift_sending_deadline')
    ) 
    context = {
        'user': user,
        'last_games': [serialize_game(game, user) for game in last_games],
        'current_games': [serialize_game(game, user) for game in current_games],
        'host_addr': host_addr
    }

    return render(request, 'user_profile/profile.html', context)


def game_toss(request, game_id):
    # TODO: вызов функции для жеребьевки
    shuffle_result = shuffle_game_participants(game_id)
    if shuffle_result:
        shuffle_result_message = f'Жеребьевка игры {game_id} проведена успешно' 
        pairs = Pair.objects.filter(game__id=game_id)
        pairs_info = '\n'.join([
            f'{pair.giver.username} - {pair.recipient.username}' 
            for pair in pairs
        ])
    else:
        shuffle_result_message = f'Жеребьевку игры {game_id} провести не удалось'
        pairs_info = ''

    return HttpResponse(f'{shuffle_result_message} {pairs_info}')

