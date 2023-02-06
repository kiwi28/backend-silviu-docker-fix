# API/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'expenses', views.ExpensesViewSet, basename='expenses')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
app_name = "API"
urlpatterns = [
    path('', include((router.urls, 'expenses'), namespace='expenses'), name='expenses'),
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework'))
]
