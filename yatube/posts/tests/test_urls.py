"""
Файл с тестами URLs проекта.
"""

from http import HTTPStatus

from django.core.cache import cache
from django.test import Client

from .tests_setup import PostsTests


class UrlTests(PostsTests):
    """
    Класс для проверки доступности страниц и шаблонов.
    """

    def setUp(self):
        """
        Создает неавторизованного и авторизованного пользователей.
        """
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        cache.clear()

    def test_urls_access(self):
        """
        Проверяет доступность страниц.
        """
        # проверка доступа на страницы для неавторизованного и
        # авторизованного пользователей
        for page_name, page_data in self.pages_dict.items():
            with self.subTest(page_name=page_name):
                if 'url' not in page_data:
                    continue
                # проверка страниц с неограниченным доступом
                if page_data['access'] == 'unlimited':
                    response = self.guest_client.get(page_data['url'])
                    self.assertEqual(response.status_code, HTTPStatus.OK)
                # проверка страниц с ограниченным доступом
                else:
                    # проверка переадресации неавторизованного пользователя
                    response = self.guest_client.get(page_data['url'])
                    self.assertEqual(response.status_code, HTTPStatus.FOUND)
                    # проверка доступа для авторизованного пользователя
                    response = self.authorized_client.get(page_data['url'])
                    if 'redirect' in page_data:
                        self.assertEqual(
                            response.status_code,
                            HTTPStatus.FOUND
                        )
                    else:
                        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_404_status(self):
        """
        Проверяет доступ к несуществующей странице.
        """
        response = self.guest_client.get('/nonexistent_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_templates(self):
        """
        Проверяет правильность шаблонов страниц.
        """
        for page_name, page_data in self.pages_dict.items():
            with self.subTest(page_name=page_name):
                if 'template' not in page_data:
                    continue
                response = self.authorized_client.get(page_data['url'])
                self.assertTemplateUsed(response, template_name=page_data[
                    'template'])
