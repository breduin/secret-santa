from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from accounts.views import UserLoginView
from .forms import GameCreateForm
from .forms import GameUpdateForm
from .forms import WishListCreateForm
from .forms import ElidiblePairCreateForm
from .models import Game
from .models import WishList


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
        return reverse_lazy('after_game_creation')
    
    def form_valid(self, form):
        game = form.save(commit=False)
        user = self.request.user
        game.created_by = user
        game.save()
        if game.is_creator_participant:
            game.participants.add(user)
            game.administrators.add(user)
            game.save()
        host_addr = self.request._current_scheme_host
        print(host_addr)
        # host = self.request.host
        game_id = game.pk
        joining_url = f'{host_addr}/joining_the_game/{game_id}'
        return render(self.request, 'after_game_creation.html', context={'joining_url': joining_url})
        # return HttpResponseRedirect(self.get_success_url())
    

class UpdateGameView(LoginRequiredMixin, UpdateView):
    """Редактировать игру."""
    model = Game
    template_name = 'create_update_game.html'
    form_class = GameUpdateForm   

    def get(self, request, *args, **kwargs):
        """
        Проверить, является ли пользователь создателем 
        игры или её администратором.
        """
        get_super = super().get(request, *args, **kwargs)
        user = request.user
        obj = self.object
        # TODO сделать проверку: редактировать может только автор или админ игры
        admins = list(obj.participants.values_list('id', flat=True))
        if user == obj.created_by or user.id in admins:             
            return get_super
        return get_super

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])

    def form_valid(self, form):
        game = form.save(commit=False)
        user = self.request.user
        if not game.is_creator_participant:
            game.participants.remove(user)
            game.administrators.remove(user)
        game.save()
        form.save_m2m()
        return HttpResponseRedirect(self.get_success_url())


def game_toss(request, game_id):
    # TODO: вызов функции для жеребьевки
    print(f'Проводим жеребьевку игры {game_id}')
    # TODO: вызов функции рассылки результатов жеребьевки
    print(f'Рассылаем результаты жеребьевки игры {game_id}')
    return 


def get_error_page(request, error_code: int):
    """Получить страницу с сообщением об ошибке для данного кода ошибки."""
    message = {
        1: """Вы не можете редактировать игру, т.е. не являетесь её создателем 
              или админстратором."""
    }
    message.setdefault(error_code, 'Неизвестный код ошибки.')
    context = {
        'message': message[error_code],
    }
    return render('error.html', context)


class AfterGameCreationView(TemplateView):
    """Инфо-страницы после создания игры."""
    template_name = "after_game_creation.html"


def joining_the_game(request, game_id):
    """Страница для присоединения к игре"""
    try:
        game = Game.objects.get(pk=game_id)
    except Exception:
        raise Http404("Игра не найдена.")

    request.session['assigned_game_id'] = game_id
    return UserLoginView.as_view()(request)


class CreateUpdateWishListView(LoginRequiredMixin, UpdateView):
    """Создать список желаний."""
    login_url = reverse_lazy('login')
    template_name = 'wishlist.html'
    form_class = WishListCreateForm

    def get_object(self):
        user = self.request.user
        try:
            game_id = self.kwargs['game_id']
        except KeyError:
            raise Http404("Нет идентификатора игры.")
        try:
            game = Game.objects.get(id=game_id)
        except queryset.model.DoesNotExist:
            raise Http404("Игра не найдена.")                          

        obj, _ = WishList.objects.get_or_create(
            user=user,
            game=game
            )         
        return obj

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])


class ElidiblePairCreateView(LoginRequiredMixin, CreateView):
    """Создать список желаний."""
    login_url = reverse_lazy('login')
    template_name = 'elidible_pair.html'
    form_class = ElidiblePairCreateForm

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        try:
            game_id = self.kwargs['game_id']
        except KeyError:
            raise Http404("Нет идентификатора игры.")
        try:
            game = Game.objects.get(id=game_id)
        except queryset.model.DoesNotExist:
            raise Http404("Игра не найдена.")  
        kwargs['game_id'] = game_id
        return kwargs    

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])

    def form_valid(self, form):
        pair = form.save(commit=False)

        try:
            game_id = self.kwargs['game_id']
        except KeyError:
            raise Http404("Нет идентификатора игры.")
        try:
            game = Game.objects.get(id=game_id)
        except queryset.model.DoesNotExist:
            raise Http404("Игра не найдена.")  

        pair.game = game
        pair.save()
        return HttpResponseRedirect(self.get_success_url())        