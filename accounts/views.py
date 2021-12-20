from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import *
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView

from .forms import GameUserCreateForm
from .forms import UserLoginForm
from .forms import UserPasswordResetForm
from .forms import UserUpdateForm
from .models import User
from games.models import Game


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
        if self.request.session['assigned_game_id']:
            game_id = self.request.session.pop('assigned_game_id')
            game = Game.objects.get(pk=game_id)
            game.participants.add(self.object.pk)
            game.save_m2m()
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
        try:
            game_id = self.request.session.pop('assigned_game_id')
            game = Game.objects.get(pk=game_id)
            game.participants.add(self.request.user.pk)
            game.save_m2m()
        except KeyError:
            pass
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
    form_class = UserUpdateForm
    template_name = 'accounts/user_update.html'
    
    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])


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

