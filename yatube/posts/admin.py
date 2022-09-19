from django.contrib import admin

from .models import Post, Group, Comment, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Класс для кастомизации админки модели Роst.
    """

    list_display = (
        'pk',
        'text',
        'pub_date',
        'author',
        'group',
    )
    # Интерфейс для выбора сообщества
    list_editable = ('group',)
    # Интерфейс для поиска по тексту постов
    search_fields = ('text',)
    # Фильтрация по дате
    list_filter = ('pub_date',)
    # Вывод строки в случае отсутствия данных в записи
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """
    Класс для кастомизации админки модели Group.
    """

    list_display = (
        'pk',
        'title',
        'slug',
        'description',
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Класс для кастомизации админки модели Follow.
    """

    list_display = (
        'user',
        'author',
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Класс для кастомизации админки модели Comment.
    """

    list_display = (
        'post',
        'author',
        'text',
        'created',
    )
