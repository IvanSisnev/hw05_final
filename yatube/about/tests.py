"""
Файл с тестами страниц приложения about.
"""

from http import HTTPStatus
from typing import Dict

from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()


class UrlTests(TestCase):
    """
    Класс для проверки доступности страниц и шаблонов.
    """

    def setUp(self):
        """
        Создает неавторизованного пользователя.
        """
        self.guest_client = Client()

    def test_urls_templates(self):
        """
        Проверяет доступность страниц и корректность шаблонов.
        """
        urls_templates: Dict[str, str] = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/techno.html',
        }
        for url, template in urls_templates.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template_name=template)
