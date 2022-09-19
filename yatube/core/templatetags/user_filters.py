from django import template

register = template.Library()


@register.filter
def addclass(field, css):
    """
    Добавить в шаблон аттрибут класса для поля формы.
    """
    return field.as_widget(attrs={'class': css})
