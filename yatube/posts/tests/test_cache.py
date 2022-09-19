"""
Файл с тестами кеширования страниц.
"""
from django.core.cache import cache
from django.test import Client
from django.urls import reverse

from .tests_setup import PostsTests


class CacheTests(PostsTests):
    """
    Класс для проверки правильности работы кеширования.
    """

    def setUp(self):
        """
        Создает авторизованного пользователя.
        """
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_cache(self):
        """
        Проверяет правильность кеширования главной страницы.
        """

        def get_response():
            return self.authorized_client.get(reverse('posts:index'))

        text = self.post.text
        # запись есть на странице
        self.assertContains(get_response(), text)
        # удаление записи
        self.post.delete()
        # запись есть на кешированной странице
        self.assertContains(get_response(), text)

        cache.clear()
        # записи нет на странице
        self.assertNotContains(get_response(), text)
