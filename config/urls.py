# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Создаем схему для Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version='v1',
        description="API для трекера привычек (Atomic Habits)",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@habits.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Корневой URL - HTML страница
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # Админ-панель Django
    path('admin/', admin.site.urls),

    # API эндпоинты для привычек
    path('api/habits/', include('habits.urls')),

    # API эндпоинты для пользователей
    path('api/users/', include('users.urls')),

    # JWT аутентификация
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Документация API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]