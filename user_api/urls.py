# urls.py
from django.urls import path
from .views import UserRegisterView, login_view, logout_view, UserProfileCreateView

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserProfileCreateView.as_view(), name='profile-create'),
]
