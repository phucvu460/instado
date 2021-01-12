from django.urls import path
from . import views
from .views import PostListView,UserPostListView

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path("post/<int:post_id>", views.post, name='post'),
    path("like_post/<int:post_id>", views.like, name='like'),
    path("create_post", views.create_post, name='create_post'),
    path("user_posts/<str:username>", UserPostListView.as_view(), name='user_posts'),


]

