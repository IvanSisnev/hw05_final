from django.views.generic import TemplateView


class AboutAuthorView(TemplateView):
    """
    Класс для отображения страницы об авторе.
    """
    template_name = 'about/author.html'


class AboutTechView(TemplateView):
    """
    Класс для отображения страницы о технологиях сайта.
    """
    template_name = 'about/techno.html'
