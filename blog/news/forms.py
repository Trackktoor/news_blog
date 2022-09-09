from django import forms

class CreatePostForm(forms.Form):
    title = forms.CharField(label='Название статьи', max_length=100)
    content = forms.CharField(label='Текст поста', widget=forms.Textarea)

class ChangePostForm(forms.Form):
    title = forms.CharField(label='Название статьи', max_length=100)
    content = forms.CharField(label='Текст поста', widget=forms.Textarea)

class CommentPostForm(forms.Form):
    comment_body = forms.CharField(widget=forms.Textarea)