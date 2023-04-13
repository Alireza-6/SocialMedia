from django.db.models import QuerySet

from blog.filters import PostFilter
from blog.models import Post, Subscription
from users.models import BaseUser


def post_list(*, filters=None, user: BaseUser, self_include: bool = True) -> QuerySet[Post]:
    filters = filters or {}
    subscriptions = list(Subscription.objects.filter(subscriber=user).values_list("target", flat=True))
    if self_include:
        subscriptions.append(user.id)
    if subscriptions:
        qs = Post.objects.filter(author__in=subscriptions)
        return PostFilter(filters, qs).qs
    return Post.objects.none()


def post_detail(*, slug: str, user: BaseUser, self_include: bool = True) -> Post:
    subscriptions = list(Subscription.objects.filter(subscriber=user).values_list("target", flat=True))
    if self_include:
        subscriptions.append(user.id)
    return Post.objects.get(slug=slug, author__in=subscriptions)


def get_subscribers(*, user: BaseUser) -> QuerySet[Subscription]:
    return Subscription.objects.filter(subscriber=user)
