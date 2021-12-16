import random

from django.shortcuts import render

# Create your views here.

from games.models import Game


def get_game_participants(game_id):
    participants = list(Game.objects.filter(pk=game_id).values_list('participants', flat=True))
    return participants



def test(request):
    participants = get_game_participants(game_id=1)
    if participants:
        print('ok')
    print(len(participants))
    print(participants)
    random.shuffle(participants)
    print(participants)
    pass