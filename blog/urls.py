from django.urls import path

from blog.apis.post import PostApi, PostDetailApi
from blog.apis.subscription import SubscribeApi, SubscribeDetailApi

urlpatterns = [
    path("post/", PostApi.as_view(), name="post"),
    path("post/<slug:slug>", PostDetailApi.as_view(), name="post_detail"),
    path("subscribe/", SubscribeApi.as_view(), name="subscribe"),
    path("subscribe/<str:email>", SubscribeDetailApi.as_view(), name="subscribe_detail"),
]
