"""
Файл с тестами view-функций проекта.
"""

from core.views import server_error, csrf_failure
from django.core.cache import cache
from django.test import Client
from django.urls import reverse

from .tests_setup import PostsTests
from ..models import Post, Follow


class ViewsTests(PostsTests):
    """
    Класс для проверки правильности шаблонов во view-функциях.
    """

    def setUp(self):
        """
        Создает авторизованного пользователя.
        """
        self.authorized_client = Client()
        self.authorized_client_2 = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_2.force_login(self.user_2)

        cache.clear()

    def test_views_templates(self):
        """
        Проверяет правильность шаблонов во view-функциях.
        """

        # проверка соответствия шаблонов и reverse(name)
        for page_name, page_data in self.pages_dict.items():
            with self.subTest(reverse_name=page_name):
                if 'template' not in page_data:
                    continue
                response = self.authorized_client.get(
                    reverse(page_name, kwargs=page_data['param']))
                self.assertTemplateUsed(response, page_data['template'])

    def test_views_context(self):
        """
        Проверяет правильность переданного контекста.
        """
        for page_name, page_data in self.pages_dict.items():
            with self.subTest(page_name=page_name):
                if 'context' not in page_data:
                    continue
                response = self.authorized_client.get(
                    reverse(page_name, kwargs=page_data['param'])
                )
                if 'test_method' in page_data['context']:
                    self.assertEqual(page_data['context'][
                        'test_method'](
                        response.context[
                            page_data['context']['variable']]),
                        page_data['context']['data'])
                else:
                    self.assertEqual(
                        response.context[page_data['context']['variable']],
                        page_data['context']['data'])

    def test_post(self):
        """
        Проверяет, что созданная запись отображается на нужных
        страницах.
        """

        for page_name, page_data in self.pages_dict.items():
            with self.subTest(page_name=page_name):
                if 'paginator' not in page_data:
                    continue
                response = self.authorized_client.get(reverse(
                    page_name, kwargs=page_data['param']))
                self.assertContains(response, self.post)

    def test_comment(self):
        """
        Проверяет, что добавленный комментарий отображается на странице поста.
        """
        page_name = 'posts:post_detail'
        response = self.authorized_client.get(
            reverse(page_name, kwargs=self.pages_dict[page_name]['param'])
        )
        self.assertContains(response, self.comment)

    def test_image_context(self):
        """
        Проверяет, что при выводе поста с картинкой изображение передаётся в
        контексте.
        """
        # сохранение картинки в поле поста
        self.post.image = self.test_pic_upload
        self.post.save()

        for page_name, page_data in self.pages_dict.items():
            with self.subTest(page_name=page_name):
                if 'context' not in page_data:
                    continue
                response = self.authorized_client.get(
                    reverse(page_name, kwargs=page_data['param'])
                )
                # страницы со списком записей в контексте
                if page_data['context']['variable'] == 'posts':
                    post = response.context['posts'].get(id=self.post.id)
                    self.assertEqual(post.image,
                                     f'posts/{self.test_pic_upload.name}')
                # страницы с одиночной записью в контексте
                else:
                    post = response.context[page_data['context'][
                        'variable']]
                    self.assertEqual(post.image,
                                     f'posts/{self.test_pic_upload.name}')

    def test_auth_follow(self):
        """
        Проверяет то, что авторизованный пользователь может подписываться на
        других пользователей.
        """
        # сравнение объекта Follow из БД с тестовой подпиской
        self.follow = Follow.objects.first()
        self.assertEqual(self.follow.author, self.follow.author)
        self.assertEqual(self.follow.user, self.follow.user)

    def test_unfollow(self):
        """
        Проверяет, что механизм отписки работает.
        """
        # удаление подписки и проверка удаления
        self.follow.delete()
        self.assertIsNone(Follow.objects.first())

    def test_follow_post(self):
        """
        Проверяет, что новая запись пользователя появляется в ленте тех, кто на
        него подписан и не появляется в ленте тех, кто не подписан.
        """
        # создание тестовой подписки
        form_data = {
            'user': self.user,
            'author': self.author,
        }
        self.authorized_client.post(reverse('posts:profile_follow',
                                            kwargs={'username':
                                                        self.author.username}),
                                    data=form_data, follow=True)

        # создание тестового поста для проверки подписки
        self.follow_post = Post.objects.create(
            text='Пост для проверки подписки',
            author=self.author,
        )

        # проверка наличия поста на странице подписавшегося
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertContains(response, self.follow_post)

        # проверка отсутствия поста на странице неподписавшегося
        response = self.authorized_client_2.get(reverse('posts:follow_index'))
        self.assertNotContains(response, self.follow_post)

    def test_unfollow_post(self):
        """
        Проверяет, что новая запись автора, подписка на которого отменена,
        не появляется в ленте отписавшегося.
        """

        # создание тестового поста для проверки подписки
        self.follow_post = Post.objects.create(
            text='Пост для проверки подписки',
            author=self.author,
        )

        # отмена подписки
        self.authorized_client.post(reverse(
            'posts:profile_unfollow', kwargs={
                'username': self.author.username
            }
        ))

        # проверка отсутствия поста на странице отписавшегося
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertNotContains(response, self.follow_post)

    def test_self_follow(self):
        """
        Проверяет невозможность подписки на самого себя.
        """
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        self.assertNotContains(response, reverse('posts:follow_index'))

    def test_double_follow(self):
        """
        Проверяет то, что на автора можно подписаться только один раз.
        """
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.author.username})
        )
        self.assertNotContains(response, reverse('posts:follow_index'))

    def test_403_template(self):
        """
        Проверяет кастомный шаблон 403.
        """
        response = csrf_failure(self.authorized_client.get('/'))
        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.template_name, 'core/403csrf.html')

    def test_404_template(self):
        """
        Проверяет кастомный шаблон 404.
        """
        response = self.authorized_client.get('/nonexistent_page/')
        self.assertTemplateUsed(response, template_name='core/404.html')

    def test_500_template(self):
        """
        Проверяет кастомный шаблон 500.
        """
        response = server_error(self.authorized_client.get('/'))
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.template_name, 'core/500.html')
