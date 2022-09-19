from django import forms

from .models import Post, Comment


class PostForm(forms.ModelForm):
    """
    Класс для создания формы новой записи.
    """

    class Meta:
        model = Post
        fields = ('text', 'group', 'image')


class CommentForm(forms.ModelForm):
    """
    Класс для создания формы комментария.
    """

    class Meta:
        model = Comment
        fields = ('text',)
