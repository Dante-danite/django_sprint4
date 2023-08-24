from django.contrib.auth import get_user_model
from django import forms
from .models import Post, Comment

User = get_user_model()


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'pub_date', 'category', 'image')
        widgets = {'pub_date': forms.DateTimeInput(format='%d/%m/%Y %H:%M', attrs={'type': 'datetime-local'})}


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)