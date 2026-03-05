from django import forms
from .models import Thread, ForumPost

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title']

class PostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['body']