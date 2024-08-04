# urls.py
from django.urls import path
from .views import UserRegisterView, login_view

urlpatterns = [
    path('api/login/', login_view, name='login'),
    path('api/register/', UserRegisterView.as_view(), name='register'),
]
