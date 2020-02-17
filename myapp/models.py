from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.db import IntegrityError

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=200, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    votes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)

    def upvote(self):
        self.votes += 1
        self.save()

    def downvote(self):
        self.votes -= 1
        self.save()

    def upcomment(self):
        self.comments += 1
        self.save()

    def downcomment(self):
        self.comments -= 1
        self.save()

# # https://stackoverflow.com/questions/34838034/how-to-create-a-voting-model-in-django
# class Vote(models.Model):
#     voter = models.ForeignKey(User, related_name="user_votes", on_delete="CASCADE")
#     post = models.ForeignKey(Post, related_name="post_votes", on_delete="CASCADE")
#     vote_type = models.CharField(max_length=4)
#
#     class Meta:
#         unique_together = ('voter', 'post', 'vote_type')

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=100, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    votes = models.IntegerField(default=0)

    def upvote(self):
        self.votes += 1
        self.save()

    def downvote(self):
        self.votes -= 1
        self.save()