from django import forms
from .models import Article, Comment

class ArticleForms(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CommentForms(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)