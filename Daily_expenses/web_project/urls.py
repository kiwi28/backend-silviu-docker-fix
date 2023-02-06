from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi # noqa

# from rest_framework import routers, serializers, viewsets

# schema_view = get_swagger_view(title='Daily Expenses')
schema_view = get_schema_view(
    openapi.Info(title='Daily Expenses API', default_version='v1'),
    public=True,
    # permission_classes=(permissions.IsAuthenticated,)
    permission_classes=(permissions.AllowAny,)
)

urlpatterns = [
    # path(
    #     'docs/',
    #     schema_view),
    path('admin/', admin.site.urls),
    path('', include('API.urls')),
    path('', include('categories.urls')),
    path('', include('stats.urls')),
    # path('api/register/', RegisterAPI.as_view(), name='register'),
    path('', include('accounts.urls'))
]

urlpatterns += [
    path(
        'docs/',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    )
]
