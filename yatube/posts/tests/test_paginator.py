"""
Файл с тестами паджинации страниц.
"""

from django.core.cache import cache
from django.test import Client
from django.urls import reverse

from .tests_setup import PostsTests
from ..models import Post


class PaginatorTests(PostsTests):
    """
    Класс для проверки правильности паджинации.
    """

    def setUp(self):
        """
        Создает авторизованного пользователя.
        """
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_paginator(self):
        """
        Проверить правильность работы паджинатора на страницах.
        """
        for page_name, page_data in self.pages_dict.items():
            if 'paginator' in page_data:
                response = self.authorized_client.get(reverse(page_name,
                                                              kwargs=page_data[
                                                                  'param'
                                                              ]
                                                              )
                                                      )
                # общее количество записей в базе
                total_posts = Post.objects.count()
                # максимальное количество записей на странице
                posts_per_page = response.context[
                    'page_obj'].paginator.per_page
                # список страниц с записями
                page_list = response.context['page_obj'].paginator.page_range

                for page in page_list:
                    response = self.authorized_client.get(
                        reverse(page_name,
                                kwargs=page_data['param']) + f'?page={page}')
                    if total_posts >= posts_per_page:
                        self.assertEqual(len(response.context['page_obj']),
                                         posts_per_page)
                        total_posts -= posts_per_page
                    else:
                        self.assertEqual(len(response.context['page_obj']),
                                         total_posts)
                    cache.clear()
