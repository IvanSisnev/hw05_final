from datetime import datetime


def year(request):
    """
    Добавить на шаблоны переменную с текущим годом.
    """
    year = datetime.now().year
    return {'year': year}
