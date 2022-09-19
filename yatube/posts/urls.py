from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Страница с записями сообщества
    path('group/<slug:slug>/', views.group_posts, name='group_list'),
    # Страница пользователя
    path('profile/<str:username>/', views.profile, name='profile'),
    # Страница записи
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    # Страница создания записи
    path('create/', views.post_create, name='post_create'),
    # Страница редактирования записи
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    # Страница удаления записи
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    # Страница комментирования
    path('posts/<int:post_id>/comment/', views.add_comment,
         name='add_comment'),
    # Сраница постов авторов по подписке
    path('follow/', views.follow_index, name='follow_index'),
    # Страница подписки на автора
    path('profile/<str:username>/follow/', views.profile_follow,
         name='profile_follow'),
    # Страница отмены подписки на автора
    path('profile/<str:username>/unfollow/', views.profile_unfollow,
         name='profile_unfollow'),
]
