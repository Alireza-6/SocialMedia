from django.db.models import QuerySet

from blog.models import Post, Subscription
from users.models import BaseUser


def create_post(*, user: BaseUser, title: str, content: str) -> QuerySet[Post]:
    ...


def unsubscribe(*, user: BaseUser, email: str) -> dict:
    ...


def subscribe(*, user: BaseUser, email: str) -> QuerySet[Subscription]:
    ...
