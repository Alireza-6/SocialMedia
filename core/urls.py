from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

v1_urlpatterns = [
    path('products/', include('blog.urls')),
    path('users/', include('users.urls')),
    path('jwt/', include('authentication.urls')),
]

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(api_version="v1"), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path('admin/', admin.site.urls),
    path('api/v1/', include(v1_urlpatterns)),
]
