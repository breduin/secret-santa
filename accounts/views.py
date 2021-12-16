from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import *
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView, UpdateView

from .forms import GameUserCreateForm, UserLoginForm, UserPasswordResetForm
from .models import User


def serialize_users(users):
    user_names = [f'{user.first_name} {user.last_name}' for user in users]
    return ', '.join(user_names)


def serialize_game(game, user):
    return {
        'name': game.name,
        'is_admin': user in game.administrators.all(),
        'admins': serialize_users(game.administrators.all()),
        'participants_count': game.participants.count(),
        'id': game.id,
        'created_at': game.created_at,
        'gift_cost_limit': game.get_gift_cost_limit_display(),
        'registration_deadline': game.registration_deadline,
        'gift_sending_deadline': game.gift_sending_deadline,
        'participants': serialize_users(game.participants.all()),
    }
         

def profile(request, profile_id):
    user = get_object_or_404(
        (
            User.objects
            .prefetch_related('games__administrators')
            .prefetch_related('games__participants')
        ),
        id=profile_id
    )
    
    games = user.games.all()
    context = {
        'user': user,
        'games': [serialize_game(game, user) for game in games],
    }

    return render(request, 'profile.html', context)


def game_toss(request, game_id):
    # TODO: вызов функции для жеребьевки
    print(f'Проводим жеребьевку игры {game_id}')
    # TODO: вызов функции рассылки результатов жеребьевки
    print(f'Рассылаем результаты жеребьевки игры {game_id}')
    return HttpResponse(f"Жеребьевка игры {game_id} проведена")


class UserCreateView(CreateView):
    form_class = GameUserCreateForm
    template_name = 'accounts/user_create.html'

    def __init__(self):
        self.object = None

    def get_success_url(self):
        return reverse_lazy('login')

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()

        # TODO здесь привязка пользователя к игре, если есть ссылка
        # TODO здесь проверка соглашения об обработке ПД

        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            if not request.POST.get('remember_me', None):
                request.session.set_expiry(0)
            else:
                request.session.set_expiry(settings.SESSION_EXPIRE_TIME_SPAN)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])


class UserLogoutView(LoginRequiredMixin, LogoutView):
    login_url = reverse_lazy('main_page')
    template_name = 'accounts/logout.html'
    next_page = login_url


class UserUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for user profile update
    """
    login_url = reverse_lazy('login')
    model = User
    template_name = 'accounts/user_update.html'
    context_object_name = 'user'
    fields = ['last_name', 'first_name', 'email']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
    def get_success_url(self):
        reverse_lazy('profile', args=[self.request.user.id])


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """
    View for user password change
    """
    template_name = 'accounts/user_password_change.html'
    context_object_name = 'user'
    success_url = reverse_lazy('password_change_done')


class UserPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/user_password_change_done.html'
    context_object_name = 'user'


class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'accounts/user_password_reset.html'
    context_object_name = 'user'
    email_template_name = 'accounts/user_password_reset_email_template.html'
    subject_template_name = 'accounts/user_password_reset_email_template_subject.html'
    success_url = reverse_lazy('password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/user_password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/user_password_reset_confirm.html'
    context_object_name = 'user'
    success_ucrl = reverse_lazy('password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/user_password_reset_complete.html'

