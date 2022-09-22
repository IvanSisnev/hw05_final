"""
Файл с тестами форм моделей.
"""

from typing import Dict, Any

from django import forms
from django.test import Client
from django.urls import reverse

from .tests_setup import PostsTests
from ..models import Post


class FormsTests(PostsTests):
    """
    Класс для проверки правильности форм на страницах.
    """

    def setUp(self):
        """
        Создает неавторизованного и авторизованного пользователей.
        """
        self.guest_client = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_form_fields_type(self):
        """
        Проверить правильность передаваемых форм.
        """

        form_fields: Dict[str, Any] = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }

        for page_name, page_data in self.pages_dict.items():
            if 'form' in page_data:
                response = self.authorized_client.get(
                    reverse(page_name, kwargs=page_data['param'])
                )
                for field, field_type in form_fields.items():
                    with self.subTest(field=field):
                        form_field = response.context.get('form').fields.get(
                            field)
                        self.assertIsInstance(form_field, field_type)

    def test_post_create(self):
        """
        Проверить создание новой записи.
        """
        post_count = Post.objects.count()

        form_data = {
            'text': 'Текст нового поста',
            'author': self.user,
            'group': self.group.id,
            'image': self.test_pic_upload,
        }

        self.authorized_client.post(reverse('posts:post_create'),
                                    data=form_data, follow=True)

        # проверка добавления новой записи в БД
        self.assertEqual(Post.objects.count(), post_count + 1)
        # проверка созданной записи
        post = Post.objects.first()
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.author, form_data['author'])
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(post.image, f'posts/{self.test_pic_upload.name}')

    def test_post_unauth_create_redir(self):
        """
        Проверить редирект и невозможность создания записи неавторизованным
        пользователем.
        """
        form_data = {
            'text': 'Текст нового поста гостя',
            'author': self.guest_client,
        }
        self.guest_client.post(reverse('posts:post_create'),
                               data=form_data, follow=True)
        # проверка того, что запись не создана
        post = Post.objects.first()
        self.assertNotEqual(post.text, form_data['text'])
        self.assertNotEqual(post.author, form_data['author'])

        # проверка редиректа неавторизованного пользователя
        response = self.guest_client.get(reverse('posts:post_create'))
        self.assertRedirects(response, reverse('users:login'))

    def test_post_edit(self):
        """
        Проверить редактирование существующей записи.
        """
        form_data = {
            'text': 'Отредактированный текст нового поста',
            'group': self.group.id,
            'image': '',
        }
        self.authorized_client.post(reverse('posts:post_edit',
                                            kwargs=self.pages_dict[
                                                'posts:post_edit']['param']),
                                    data=form_data, follow=True)

        # проверка успешного изменения записи
        edited_post = Post.objects.get(id=self.post.id)
        self.assertEqual(edited_post.text, form_data['text'])
        self.assertEqual(edited_post.author, self.user)
        self.assertEqual(edited_post.group.id, form_data['group'])
        self.assertEqual(edited_post.image, form_data['image'])

    def test_comment_unauth_create_redir(self):
        """
        Проверить редирект и невозможность добавления комментария
        неавторизованным пользователем.
        """
        form_data = {
            'text': 'Текст комментария',
            'author': self.guest_client,
            'post': self.post.id,
        }
        self.guest_client.post(reverse('posts:add_comment',
                                       kwargs=self.pages_dict[
                                           'posts:add_comment']['param']),
                               data=form_data, follow=True)
        # проверка того, что комментарий не добавлен
        self.assertNotEqual(self.post.comments.first(), form_data[
            'text'])

        # проверка редиректа неавторизованного пользователя
        response = self.guest_client.get(reverse('posts:add_comment',
                                                 kwargs=self.pages_dict[
                                                     'posts:add_comment'][
                                                     'param']))
        self.assertRedirects(response, reverse('users:login'))

    def test_comment_create(self):
        """
        Проверить сохранение добавленного комментария.
        """
        form_data = {
            'text': 'Текст комментария',
            'author': self.user,
            'post': self.post.id,
        }
        self.authorized_client.post(reverse('posts:add_comment',
                                            kwargs=self.pages_dict[
                                                'posts:add_comment'][
                                                'param']),
                                    data=form_data, follow=True)
        # проверка добавления комментария
        commented_post = Post.objects.get(id=self.post.id)
        comment = commented_post.comments.all().latest()
        self.assertEqual(comment.text, form_data['text'])
        self.assertEqual(comment.author, form_data['author'])
        self.assertEqual(commented_post.id, form_data['post'])
