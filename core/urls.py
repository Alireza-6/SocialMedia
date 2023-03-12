from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="SocialMedia API",
        default_version='v1',
        description="description",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

v1_urlpatterns = [
    path('products/', include('blog.apis.urls')),
]
urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/', include(v1_urlpatterns)),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
