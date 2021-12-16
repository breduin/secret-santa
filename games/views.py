from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .forms import GameCreateForm, GameUpdateForm
from .models import Game


class MainPageView(TemplateView):
    """Представление для главной страницы"""
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CreateGameView(LoginRequiredMixin, CreateView):
    """Создать игру."""
    login_url = reverse_lazy('login')
    template_name = 'create_update_game.html'
    form_class = GameCreateForm    

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])
    
    def form_valid(self, form):
        game = form.save(commit=False)
        game.created_by = self.request.user
        game.save()
        return HttpResponseRedirect(self.get_success_url())
    

class UpdateGameView(UpdateView):
    """Редактировать игру."""
    model = Game
    template_name = 'create_update_game.html'
    form_class = GameUpdateForm   

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])


def game_toss(request, game_id):
    # TODO: вызов функции для жеребьевки
    print(f'Проводим жеребьевку игры {game_id}')
    # TODO: вызов функции рассылки результатов жеребьевки
    print(f'Рассылаем результаты жеребьевки игры {game_id}')
    return 