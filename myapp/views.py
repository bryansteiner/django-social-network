from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from .forms import PostForm, CommentForm
from .models import Post, Comment
import logging
from django.contrib import messages

def home(request):
    form = PostForm()
    sort = '-date' # descending is default
    if request.method == 'POST':
        if 'post' in request.POST:
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                form = PostForm()
        elif 'newest' in request.POST:
            sort = '-date'
        elif 'oldest' in request.POST:
            sort = 'date'
        elif 'likes' in request.POST:
            sort = '-votes'
        elif 'comments' in request.POST:
            sort = '-comments'
        else:
            post = Post.objects.get(pk=request.POST['pk'])
            if 'upvote_post' in request.POST:
                post.upvote()
            elif 'downvote_post' in request.POST:
                post.downvote()
            elif 'delete_post' in request.POST:
                post.delete()
    posts = Post.objects.all().order_by(sort)
    args = {'form': form, 'posts': posts}
    return render(request, 'home.html', args)

def post(request, pk):
    post = Post.objects.get(pk=pk)
    form = CommentForm()
    sort = '-date'  # descending is default
    if request.method == 'POST':
        if 'upvote_post' in request.POST:
            post.upvote()
        elif 'downvote_post' in request.POST:
            post.downvote()
        elif 'comment' in request.POST:
            form = CommentForm(request.POST, post)
            if form.is_valid():
                post.upcomment()
                comment = form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                form = CommentForm()
        elif 'delete_post' in request.POST:
            post.delete()
            return redirect('/')
        elif 'upvote_comment' in request.POST:
            comment = Comment.objects.get(pk=request.POST['pk'])
            comment.upvote()
        elif 'downvote_comment' in request.POST:
            comment = Comment.objects.get(pk=request.POST['pk'])
            comment.downvote()
        elif 'delete_comment' in request.POST:
            post.downcomment()
            comment = Comment.objects.get(pk=request.POST['pk'])
            comment.delete()
        elif 'newest' in request.POST:
            sort = '-date'
        elif 'oldest' in request.POST:
            sort = 'date'
        elif 'likes' in request.POST:
            sort = '-votes'
    comments = Comment.objects.filter(post=post).order_by(sort)
    args = {'post': post, 'form': form, 'comments': comments}
    return render(request, 'post.html', args)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = UserCreationForm()
    args = {'form': form}
    return render(request, 'register.html', args)

def profile(request):
    if request.method == 'POST':
        if 'delete_account' in request.POST:
            user = User.objects.get(username=request.user)
            user.delete()
            return redirect('/register')
    return render(request, 'profile.html')

def myposts(request):
    if request.method == 'POST':
        post = Post.objects.get(pk=request.POST['pk'])
        if 'upvote_post' in request.POST:
            post.upvote()
        elif 'downvote_post' in request.POST:
            post.downvote()
        elif 'delete_post' in request.POST:
            post.delete()

    posts = Post.objects.filter(user=request.user)
    args = {'posts': posts}
    return render(request, 'myposts.html', args)

def search(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        if 'search_posts' in request.POST:
            posts = posts.filter(body__contains=request.POST['search_posts'])
        elif 'search_date' in request.POST:
            posts = posts.filter(date=request.POST['search_date'])
    args = {'posts': posts}
    return render(request, 'search.html', args)