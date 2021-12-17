import os

from django.core.mail import send_mass_mail, send_mail
from games.models import Pair
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

SUBJECT_TEMPLATE = 'Результаты жеребьевки игры "Тайный Санта" - "{game}"'


def create_letter_text(pair):
    # TODO: add fields to game
    # if pair.game.is_online:
    #     template_filename = 'toss_results_message_template_online.txt'
    # else:
    #     template_filename = 'toss_results_message_template_offline.txt'
    template_filename = 'toss_results_message_template_offline.txt'

    template_path = os.path.join('templates', 'static', 'templates', 'txt', 
                                 template_filename)
    with open(template_path, 'r') as file_obj:
        text_template = file_obj.read()

    wishes = 'Список желаний пуст - положись на свою интуицию!'
    if pair.recipient.wishlist.exists():
        wishes = '\n'.join([f'- {wish}' 
                           for wish in pair.recipient.wishlist.all()])
        wishes = f'Список желаний:\n{wishes}'
    santa_letter = 'Похоже получатель не написал письмо Санте :('
    if pair.recipient.letters_to_santa.exists():
        santa_letter = (pair.recipient.letters_to_santa
                        .order_by('-created_at').first())
    return text_template.format(
        giver_name=pair.giver.first_name,
        game_name=pair.game.name,
        recipient_full_name=f'{pair.recipient.first_name} {pair.recipient.last_name}',
        deadline=pair.game.gift_sending_deadline,
        recipient_name=pair.recipient.first_name,
        recipient_email=pair.recipient.email,
        santa_letter=santa_letter,
        whislist=wishes,
        # TODO: add fields to game
        party_address='Москва, ул. Возвиженка, д.1',
    )


def send_toss_result(game_id):
    
    pairs = Pair.objects.filter(game__id=game_id).select_related()
    if not pairs.exists():
        return False, 0

    messages = []

    for pair in pairs:
        subject = SUBJECT_TEMPLATE.format(game=pair.game.name)
        email_to = pair.giver.email
        email_text = create_letter_text(pair)

        messages.append([
            subject,
            email_text,
            None,
            [email_to],
        ])

    # WARNING: mass mailing is disabled to avoid mail account block!
    # send_count = send_mass_mail(tuple(messages), fail_silently=False)
    send_count = send_mail(*messages[0], fail_silently=False)
    return True, send_count


def mass_mailing(request, game_id):
    mailing_result, count = send_toss_result(game_id)
    if mailing_result:
        mailing_result_message = (f'Участникам игры {game_id} отправлено '
                                  f'{count} писем')
    else:
        mailing_result_message = ('Не удалось выполнить рассылку писем '
                                  f'участникам игры {game_id} выполнена')

    return HttpResponse(f'{mailing_result_message}')


def pair_mailing(request, game_id, user_id):
    pair = get_object_or_404(Pair, game__id=game_id, giver__id=user_id)

    send_count = send_mail(
        SUBJECT_TEMPLATE.format(game=pair.game.name),
        create_letter_text(pair),
        None,
        [pair.giver.email],
    )
    
    return HttpResponseRedirect(reverse('profile', args=(user_id,)))
