"""
    Created by minul on 3/3/21
"""
from django import forms
from . models import Blog, Comment, User


class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["first_name", "username", "email"]


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["title", "post"]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'comment']
