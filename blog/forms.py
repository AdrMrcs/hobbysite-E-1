from django import forms
from .models import Article, Comment

class ArticleForms(forms.ModelForm):
    class Meta:
        model = Article
        field = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].disabled = True

class CommentForms(forms.ModelForm):
    class Meta:
        model = Comment
        field = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)