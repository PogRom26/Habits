# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserRegistrationView,
    UserProfileView,
    UserListView,
    TelegramConnectView,
    CustomTokenObtainPairView
)

urlpatterns = [
    # Регистрация нового пользователя
    path('register/', UserRegistrationView.as_view(), name='register'),

    # Авторизация (JWT токены)
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Профиль пользователя
    path('profile/', UserProfileView.as_view(), name='profile'),

    # Список пользователей (только для администраторов)
    path('list/', UserListView.as_view(), name='user-list'),

    # Подключение Telegram
    path('connect-telegram/', TelegramConnectView.as_view(), name='connect-telegram'),
]