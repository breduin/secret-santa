import random

from games.models import Game, Pair


def get_game_participants(game_id):
    participants = list(Game.objects.filter(pk=game_id, is_participants_shuffled=False)
                        .values_list('participants', flat=True))
    if not participants:
        return None
    return participants


def get_shuffle_participant_pairs(participants_id):
    pairs = []
    random.shuffle(participants_id)
    if len(participants_id) <= 2:
        return None
    for participant in range(len(participants_id)):
        pairs.append([participants_id[participant-1], participants_id[participant]])
    return pairs


def save_shuffled_participants(participant_pairs, game_id):
    pairs = []
    for pair in participant_pairs:
        pairs.append(Pair(giver_id=pair[0],
                          recipient_id=pair[1],
                          game_id=game_id)
                     )
    Pair.objects.bulk_create(pairs)
    Game.objects.filter(pk=game_id).update(is_participants_shuffled=True)
    return True


def shuffle_game_participants(game_id):
    participants = get_game_participants(game_id=game_id)
    if not participants or len(participants) < 3:
        raise IndexError("Can't shuffle. Participants always shuffled"
                         " or no game participants"
                         " or number of participants < 3")
    participant_pairs = get_shuffle_participant_pairs(participants)
    if save_shuffled_participants(participant_pairs=participant_pairs, game_id=game_id):
        return True
    return False

