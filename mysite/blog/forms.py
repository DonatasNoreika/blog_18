from django import forms
from .models import Comment, CustomUser
from django.contrib.auth.forms import UserCreationForm

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']