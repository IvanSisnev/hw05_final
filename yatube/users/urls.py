from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
)
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # Страница регистрации нового пользователя.
    path(
        'signup/', views.SignUp.as_view(),
        name='signup'
    ),
    # Страница выхода из учетной записи.
    path(
        'logout/',
        LogoutView.as_view(template_name='users/logged_out.html'),
        name='logout'
    ),
    # Страница входа в учетную запись.
    path(
        'login/', LoginView.as_view(template_name='users/login.html'),
        name='login'
    ),
    # Страница смены пароля.
    path(
        'password_change/', PasswordChangeView.as_view(
            template_name='users/password_change_form.html'),
        name='password_change'
    ),
    # Страница сообщения об удачной смене пароля.
    path(
        'password_change/done/', PasswordChangeDoneView.as_view(
            template_name='users/password_change_done.html'),
        name='password_change_done'
    ),
    # Страница сброса пароля.
    path('password_reset/', PasswordResetView.as_view(),
         name='password_reset'),
]
