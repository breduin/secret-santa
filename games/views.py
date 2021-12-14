from django.views.generic.base import TemplateView


class MainPageView(TemplateView):
    """Представление для главной страницы"""
    template_name = "start.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context