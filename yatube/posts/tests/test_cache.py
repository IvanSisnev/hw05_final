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
            """
            Забирает response с главной страницы.
            """
            return self.authorized_client.get(reverse('posts:index'))

        # список постов со страницы
        page_content = get_response().context['page_obj'].object_list
        # самый свежий пост
        post_to_test = page_content[0]
        # сравнения по полям с последним созданным постом
        self.assertEqual(post_to_test.text, self.post.text)
        self.assertEqual(post_to_test.author, self.post.author)
        self.assertEqual(post_to_test.group, self.post.group)

        self.post.delete()

        # обращение к главной странице и сравнение состояний
        page_content_cached = get_response().context['page_obj'].object_list
        self.assertEqual(page_content, page_content_cached)

        cache.clear()

        # повторное обращение к главной странице и сравнение
        page_content_reloaded = get_response().context['page_obj'].object_list
        self.assertNotEqual(page_content, page_content_reloaded)
