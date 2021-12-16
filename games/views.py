from django.views.generic.base import TemplateView


class MainPageView(TemplateView):
    """Представление для главной страницы"""
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def game_toss(request, game_id):
    # TODO: вызов функции для жеребьевки
    print(f'Проводим жеребьевку игры {game_id}')
    # TODO: вызов функции рассылки результатов жеребьевки
    print(f'Рассылаем результаты жеребьевки игры {game_id}')
    return 