from django.urls import reverse_lazy  # type: ignore
from django.views.generic import CreateView  # type: ignore

from .forms import CreationForm


class SignUp(CreateView):
    """
    Класс для регистрации новых пользователей.
    """
    form_class = CreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/signup.html'
