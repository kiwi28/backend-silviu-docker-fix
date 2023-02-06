from .views import RegisterAPI, LoginAPI
from knox import views as knox_views
from django.urls import path
from .views import RegisterAPI, LoginAPI, ManageUserAPI # noqa

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('profile/', ManageUserAPI.as_view(), name='profile'),
]
