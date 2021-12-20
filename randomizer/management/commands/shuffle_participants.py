import datetime

from django.core.management import BaseCommand

from games.models import Game
from randomizer.randomizer import shuffle_game_participants


class Command(BaseCommand):
    help = 'Shuffle game participants'

    def handle(self, *args, **options):
        games = Game.objects.\
            filter(is_participants_shuffled=False, registration_deadline__lte=datetime.date.today()).\
            values_list('pk', flat=True)
        for game in games:
            if shuffle_game_participants(game_id=game):
                print(f'Game with id - {game} shuffled')
                continue
            print(f"Can't shuffle game with id - {game}")
        print('Shuffle complete')

