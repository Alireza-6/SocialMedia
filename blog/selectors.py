from django.db.models import QuerySet

from blog.models import Post
from users.models import BaseUser


def post_list(*, filters=None, user: BaseUser, self_include: bool = True) -> QuerySet[Post]:
    ...


def post_detail(*, slug: str, user: BaseUser, self_include: bool = True) -> Post:
    ...
