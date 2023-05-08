from django.urls import reverse
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from blog.models import Post
from blog.selectors import post_list, post_detail
from blog.services import create_post
from core.mixins import ApiAuthMixin


class PostApi(ApiAuthMixin, APIView):
    class FilterSerializer(serializers.Serializer):
        title = serializers.CharField(required=False, max_length=100)
        search = serializers.CharField(required=False, max_length=100)
        created_at__range = serializers.CharField(required=False, max_length=100)
        author__in = serializers.CharField(required=False, max_length=100)
        slug = serializers.CharField(required=False, max_length=100)
        content = serializers.CharField(required=False, max_length=1000)

    class InputSerializer(serializers.Serializer):
        content = serializers.CharField(max_length=1000)
        title = serializers.CharField(max_length=100)

    class OutputSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")
        url = serializers.SerializerMethodField("get_url")

        class Meta:
            model = Post
            fields = ("url", "title", "author")

        def get_author(self, post):
            return post.author.email

        def get_url(self, post):
            request = self.context.get("request")
            path = reverse("blog:post_detail", args=(post.slug,))
            return request.build_absolute_uri(path)

    @extend_schema(request=InputSerializer, responses=OutputSerializer)
    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            query = create_post(
                user=request.user,
                title=serializer.validated_data.get("title"),
                content=serializer.validated_data.get("content")
            )
        except Exception as ex:
            return Response({"detail": f"Database Error - " + str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.OutputSerializer(query, context={"request": request}).data)

    @extend_schema(parameters=[FilterSerializer], responses=OutputSerializer)
    def get(self, request):
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)
        try:
            query = post_list(filters=filters_serializer.validated_data, user=request.user)
        except Exception as ex:
            return Response({"detail": f"Filter Error - " + str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.OutputSerializer(query, context={"request": request}, many=True).data)


class PostDetailApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.ModelSerializer):
        author = serializers.SerializerMethodField("get_author")

        class Meta:
            model = Post
            fields = ("author", "slug", "title", "content", "created_at", "updated_at")

        def get_author(self, post):
            return post.author.email

    @extend_schema(responses=OutputSerializer)
    def get(self, request, slug):
        try:
            query = post_detail(slug=slug, user=request.user)
        except Exception as ex:
            return Response({"detail": f"Filter Error - " + str(ex)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.OutputSerializer(query).data)
