from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import LetterToSanta
from .forms import LetterToSantaForm


class LetterToSantaCreateView(LoginRequiredMixin, CreateView):
    """Создать игру."""
    login_url = reverse_lazy('login')
    template_name = 'letter_to_santa_create.html'
    form_class = LetterToSantaForm    

    def get_success_url(self):
        return reverse_lazy('profile', args=[self.request.user.id])
    
    def form_valid(self, form):
        letter = form.save(commit=False)
        user = self.request.user
        letter.created_by = user
        letter.save()
        return HttpResponseRedirect(self.get_success_url())