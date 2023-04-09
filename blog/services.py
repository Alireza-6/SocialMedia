from django.db.models import QuerySet

from blog.models import Post
from users.models import BaseUser


def create_post(*, user: BaseUser, title: str, content: str) -> QuerySet[Post]:
    ...
