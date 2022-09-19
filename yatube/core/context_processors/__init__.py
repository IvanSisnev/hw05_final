from datetime import datetime


def year():
    """
    Добавить переменную с текущим годом.
    """
    year = datetime.now().year
    return {'year': year}
