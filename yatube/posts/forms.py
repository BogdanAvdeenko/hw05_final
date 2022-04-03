from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('group', 'text', 'image')

    def clean_subject(self):
        data = self.cleaned_data['text']
        if not data == '':
            return data
        raise forms.ValidationError('Пожалуйста, заполните поле.')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    def clean_subject(self):
        data = self.cleaned_data['text']
        if not data == '':
            return data
        raise forms.ValidationError('Пожалуйста, заполните поле.')
