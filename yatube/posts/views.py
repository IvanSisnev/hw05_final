from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import cache_page

from .forms import PostForm, CommentForm
from .models import Post, Group, User, Follow


def paginate(request, posts):
    """
    Создать из списка записей объект для паджинации.
    """
    paginator = Paginator(posts, settings.PAGE_NUM)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)


def index(request):
    """
    Обработать запрос перехода на главную страницу.
    """
    template = 'posts/index.html'

    # кеширование
    posts = cache.get('index_page')
    if not posts:
        posts = Post.objects.all()
        cache.set('index_page', posts, settings.CACHES['default']['TIMEOUT'])

    page_obj = paginate(request, posts)
    context: dict = {
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    """
    Обработать запрос перехода на страницу с записями сообщества.
    """
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = paginate(request, posts)

    context: dict = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    """
    Обработать запрос перехода на страницу пользователя.
    """
    template = 'posts/profile.html'
    user = get_object_or_404(User, username=username)
    posts = user.posts.all()
    page_obj = paginate(request, posts)

    # количество подписчиков
    num_of_followers = user.following.count()
    # количество подписок
    num_of_following = user.follower.count()
    # проверка имеющейся подписки
    following = user.following.filter(user_id=request.user.id).exists()

    context: dict = {
        'author': user,
        'posts': posts,
        'page_obj': page_obj,
        'following': following,
        'num_of_followers': num_of_followers,
        'num_of_following': num_of_following,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    """
    Обработать запрос перехода на страницу записи.
    """
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, pk=post_id)
    user = post.author
    total_posts_count = user.posts.count()
    comments = post.comments.all()
    comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'total_posts_count': total_posts_count,
    }
    return render(request, template, context)


@login_required(redirect_field_name=None)
def post_create(request):
    """
    Обработать запрос создания новой записи.
    """
    template = 'posts/create_post.html'

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    if form.is_valid():
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        return redirect('posts:profile', username=request.user.username)

    context = {'form': form}

    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    """
    Обработать запрос редактирования записи.
    """
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        return redirect('posts:post_detail', post_id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id)

    template = 'posts/create_post.html'

    context = {
        'is_edit': True,
        'template': template,
        'post': post,
        'form': form,
    }

    return render(request, template, context)


@login_required
def post_delete(request, post_id):
    """
    Обработать запрос удаления записи.
    """
    kill_post = get_object_or_404(Post, pk=post_id)
    kill_post.delete()

    return redirect('posts:profile', username=request.user.username)


@login_required(redirect_field_name=None)
def add_comment(request, post_id):
    """
    Обработать запрос комментирования записи.
    """
    post = get_object_or_404(Post, pk=post_id)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """
    Обработать запрос перехода на страницу с записями выбранных авторов.
    """
    template = 'posts/follow.html'
    posts = Post.objects.filter(author__following__user=request.user)
    page_obj = paginate(request, posts)

    context: dict = {
        'posts': posts,
        'page_obj': page_obj,
    }
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """
    Обработать запрос на подписку на автора.
    """
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    """
    Обработать запрос на отмену подписки.
    """
    author = get_object_or_404(User, username=username)
    no_follow = get_object_or_404(Follow, user=request.user, author=author)
    no_follow.delete()
    return redirect('posts:profile', username=username)
