# users/views.py
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    TelegramConnectSerializer
)

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавляем пользовательские поля в токен
        token['email'] = user.email
        token['username'] = user.username
        token['is_staff'] = user.is_staff

        return token


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserRegistrationView(generics.CreateAPIView):
    """Регистрация нового пользователя"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Профиль текущего пользователя"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """Список пользователей (только для администраторов)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = None  # или добавьте пагинацию если нужно


class TelegramConnectView(APIView):
    """Подключение Telegram аккаунта"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TelegramConnectSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.telegram_id = serializer.validated_data['telegram_id']
            user.telegram_username = serializer.validated_data.get('telegram_username')
            user.save()

            return Response(
                {'message': 'Telegram account connected successfully'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)