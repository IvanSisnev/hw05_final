"""
Файл с тестами моделей проекта.
"""

from typing import Dict

from .tests_setup import PostsTests


class PostModelTest(PostsTests):
    """
    Класс тестирования модели Post.
    """

    def test_object_name(self):
        """
        Результат метода __str__ совпадает с ожидаемым.
        """
        # для модели Post
        self.assertEqual(str(self.post), f'{self.post.text[:15]}')

        # для модели Group
        self.assertEqual(str(self.group), f'{self.group.title}')

    def test_post_verbose(self):
        """
        Наименования полей в модели Post совпадают с ожидаемыми.
        """
        post_field_verbose: Dict[str, str] = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор поста',
            'group': 'Сообщество',
        }
        for field, expected_value in post_field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(self.post._meta.get_field(field).verbose_name,
                                 expected_value)

    def test_group_verbose(self):
        """
        Наименования полей в модели Group совпадают с ожидаемыми.
        """
        group_field_verbose: Dict[str, str] = {
            'title': 'Название группы',
            'slug': 'Слаг группы',
            'description': 'Описание группы',
        }
        for field, expected_value in group_field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(self.group._meta.get_field(
                    field).verbose_name, expected_value)

    def test_post_help_text(self):
        """
        Вспомогательные тексты в модели Post совпадают с ожидаемыми.
        """
        post_help_text: Dict[str, str] = {
            'text': 'Поле для текста поста',
            'author': 'Выберите автора',
            'group': 'Необязательно: выберите сообщество',
        }
        for field, expected_value in post_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(self.post._meta.get_field(field).help_text,
                                 expected_value)

    def test_group_help_text(self):
        """
        Вспомогательные тексты в модели Group совпадают с ожидаемыми.
        """
        group_help_text: Dict[str, str] = {
            'title': 'Поле для названия сообщества',
            'slug': 'Короткий универсальный идентификатор сообщества',
            'description': 'Поле для короткого описания сообщества',
        }
        for field, expected_value in group_help_text.items():
            with self.subTest(field=field):
                self.assertEqual(self.group._meta.get_field(field).help_text,
                                 expected_value)
