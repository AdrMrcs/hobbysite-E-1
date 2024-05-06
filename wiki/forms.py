from django import forms

from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'entry', 'headerImage']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CommentForms(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['entry']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)