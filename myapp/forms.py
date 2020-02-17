from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Post
        fields = ['body']

# class VoteForm(forms.ModelForm):
#     vote_type = forms.CharField(widget=forms.RadioSelect)
#
#     class Meta:
#         model = Vote
#         fields = ['vote_type']

class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea, label='')

    class Meta:
        model = Comment
        fields = ['body']
        exclude = ('post',)