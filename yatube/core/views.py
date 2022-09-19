from django.shortcuts import render
from django.template.response import TemplateResponse

def page_not_found(request, exception):
    """
    Отработать ответ "страница не найдена".
    """
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def csrf_failure(request, reason=''):
    """
    Отработать ответ "запрос отклонен".
    """
    response = TemplateResponse(request, 'core/403csrf.html', status=403)
    return response


def server_error(request, reason=''):
    """
    Отработать ответ "ошибка сервера".
    """
    response = TemplateResponse(request, 'core/500.html', status=500)
    return response
