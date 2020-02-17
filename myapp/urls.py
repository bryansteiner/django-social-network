from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post, Comment
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    #url(r'^$', ListView.as_view(queryset=Post.objects.all().order_by("-date"), template_name='home.html'), name='home'),
    url(r'^(?P<pk>\d+)$', views.post, name='post'),
    # url(r'^(?P<pk>\d+)$', ListView.as_view(queryset=Comment.objects.all().order_by("-date"), template_name='post.html'), name='post'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^myposts/$', views.myposts, name='myposts'),
    url(r'^search/$', views.search, name='search')
]
