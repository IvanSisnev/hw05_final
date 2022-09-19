"""
Модуль для создания классов моделей.
"""

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Post(models.Model):
    """
    Класс модели Post для создания и редактирования записей.
    """

    text = models.TextField(verbose_name='Текст поста',
                            help_text='Поле для текста поста')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts',
                               verbose_name='Автор поста',
                               help_text='Выберите автора')
    group = models.ForeignKey('Group', on_delete=models.SET_NULL,
                              related_name='posts', blank=True, null=True,
                              verbose_name='Сообщество',
                              help_text='Необязательно: выберите сообщество')
    image = models.ImageField('Картинка', upload_to='posts/', blank=True,
                              help_text='Для загрузки изображения нажмите на '
                                        '"Выбрать файл"')

    class Meta:
        """
        Мета класс модели.
        """
        ordering = ['-pub_date']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        """
        Вернуть строку длиной 15 символов из текста записи.
        """
        return self.text[:15]


class Group(models.Model):
    """
    Класс модели Group для создания и редактирования сообществ.
    """

    title = models.CharField(max_length=200, verbose_name='Название группы',
                             help_text='Поле для названия сообщества')
    slug = models.SlugField(unique=True, verbose_name='Слаг группы',
                            help_text='Короткий универсальный идентификатор '
                                      'сообщества')
    description = models.TextField(verbose_name='Описание группы',
                                   help_text='Поле для короткого описания '
                                             'сообщества')

    def __str__(self):
        """
        Вернуть строку с наименованием сообщества.
        """
        return self.title


class Comment(models.Model):
    """
    Класс модели Comment для комментирования записей.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField(verbose_name='Текст комментария',
                            help_text='Напишите ваш комментарий здесь')
    created = models.DateTimeField(auto_now_add=True,
                                   verbose_name='Дата создания комментария')

    class Meta:
        """
        Мета класс модели.
        """
        ordering = ['-created']
        get_latest_by = ['created']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """
        Вернуть строку c текстом комментария.
        """
        return self.text


class Follow(models.Model):
    """
    Класс модели Follow для подписки авторов.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following')
