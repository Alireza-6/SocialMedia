from django.urls import path

from blog.apis.post import PostApi, PostDetailApi

urlpatterns = [
    path("post/", PostApi.as_view(), name="post"),
    path("post/<slug:slug>", PostDetailApi.as_view(), name="post_detail"),
]
