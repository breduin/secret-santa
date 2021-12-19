import random

from games.models import Game, Pair
from games.models import ElidiblePair
from accounts.models import User

def get_game_participants(game_id):
    participants = list(Game.objects.filter(pk=game_id, is_participants_shuffled=False)
                        .values_list('participants', flat=True))
    if not participants:
        return None
    return participants


def get_pairs_with_exclusions(participants_id, game_id, excl_pairs):
    """Получить пары участников с учётом пар-исключений."""
    participants = participants_id

    excl_users_pair = []
    for pair in excl_pairs:
        id_1 = pair.user_1.id
        participants.remove(id_1)

        id_2 = pair.user_2.id
        participants.remove(id_2)

        excl_users_pair.append([id_1, id_2])

    excl_users_allocated = []
    for pair in excl_users_pair:
        random_user = random.choice(participants)
        participants.remove(random_user)
        pair.insert(1, random_user)
        excl_users_allocated += pair

    participants_allocated = participants + excl_users_allocated
    pairs = []
    for participant in range(len(participants_allocated)):
        pairs.append(
            [participants_allocated[participant-1], participants_allocated[participant]]
            )
    return pairs


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
        return False

    excl_pairs = ElidiblePair.objects.filter(game__id=game_id)
    if excl_pairs.count() > 0:
        participant_pairs = get_pairs_with_exclusions(participants, game_id, excl_pairs)
    else:    
        participant_pairs = get_shuffle_participant_pairs(participants)

    if save_shuffled_participants(participant_pairs=participant_pairs, game_id=game_id):
        return True
    return False


def delete_shuffled_participants(game_id):
    try:
        Pair.objects.filter(game_id=game_id).delete()
        Game.objects.filter(pk=game_id).update(is_participants_shuffled=False)
        return True
    except TypeError:
        return False

