from django.urls import path

from users.apis.users import RegisterApi, ProfileApi

urlpatterns = [
    path('register/', RegisterApi.as_view(), name='register'),
    path('profile/', ProfileApi.as_view(), name='profile'),
]
