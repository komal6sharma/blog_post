from django import forms
from .models import BlogPost
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Comment

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
