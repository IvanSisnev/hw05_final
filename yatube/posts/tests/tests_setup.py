"""
Файл с установками и фикстурами для тестов.
"""
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from ..models import Post, Group, Comment, Follow

User = get_user_model()

TEMP_MEDIA_DIR = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_DIR)
class PostsTests(TestCase):
    """
    Родительский класс с созданием фикстур для классов тестов.
    """

    @classmethod
    def setUpClass(cls):
        """
        Создает фикстуры тестов модели.
        """

        super().setUpClass()
        # создание тестовых пользователей пользователя
        cls.user = User.objects.create_user(username='NoName')
        cls.user_2 = User.objects.create_user(username='NoName_2')
        cls.author = User.objects.create_user(username='TestAuthor')

        # создание тестовой группы
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test_slug',
            description='Тестовое описание',
        )

        # создание и сохранение тестовой картинки
        test_pic = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.test_pic_upload = SimpleUploadedFile(
            name='test_pic.gif',
            content=test_pic,
            content_type='image/gif',
        )

        # создание нужного количества тестовых записей
        post_list = []
        for i in range(14):
            post_list.append(Post(
                text=f'Тестовая запись - текст поста {i}',
                author=cls.user,
                group=cls.group,
            ))
        Post.objects.bulk_create(post_list)
        cls.post = Post.objects.first()

        # создание тестового комментария
        cls.comment = Comment.objects.create(
            text='Тестовый комментарий',
            post=cls.post,
            author=cls.user,
        )

        # создание тестовой подписки
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.author,
        )

        # словарь, в котором ключ это name_space:name, а значение - словарь с
        # url-aдресом, параметром адреса, шаблоном страницы, уровнем
        # доступа к странице, наличием паджинатора, параметрами для проверки
        # контекста
        cls.pages_dict = {
            'posts:index': {
                'url': '/',
                'param': None,
                'template': 'posts/index.html',
                'access': 'unlimited',
                'paginator': True,
                'context': {
                    'variable': 'posts',
                    'test_method': list,
                    'data': list(Post.objects.all())
                }
            },
            'posts:post_create': {
                'url': '/create/',
                'param': None,
                'template': 'posts/create_post.html',
                'form': True,
                'access': 'limited',
            },
            'posts:profile': {
                'url': f'/profile/{cls.user.username}/',
                'param': {'username': cls.user.username},
                'template': 'posts/profile.html',
                'access': 'unlimited',
                'paginator': True,
                'context': {
                    'variable': 'posts',
                    'test_method': list,
                    'data': list(cls.user.posts.all())
                }
            },
            'posts:group_list': {
                'url': f'/group/{cls.group.slug}/',
                'param': {'slug': cls.group.slug},
                'template': 'posts/group_list.html',
                'access': 'unlimited',
                'paginator': True,
                'context': {
                    'variable': 'posts',
                    'test_method': list,
                    'data': list(cls.group.posts.all()),
                }
            },
            'posts:post_detail': {
                'url': f'/posts/{cls.post.id}/',
                'param': {'post_id': cls.post.id},
                'template': 'posts/post_detail.html',
                'access': 'unlimited',
                'context': {
                    'variable': 'post',
                    'data': Post.objects.get(pk=cls.post.id),
                }
            },
            'posts:post_edit': {
                'url': f'/posts/{cls.post.id}/edit/',
                'param': {'post_id': cls.post.id},
                'template': 'posts/create_post.html',
                'form': True,
                'access': 'limited',
                'context': {
                    'variable': 'post',
                    'data': Post.objects.get(pk=cls.post.id),
                }
            },
            'posts:add_comment': {
                # 'url': f'/posts/{cls.post.id}/comment/',
                'param': {'post_id': cls.post.id},
                # 'template': 'posts/post_detail.html',
                'access': 'limited',
            }
        }

    @classmethod
    def tearDownClass(cls):
        """
        Приборка после тестов.
        """
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_DIR, ignore_errors=True)
