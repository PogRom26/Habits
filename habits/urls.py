# habits/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (
    HabitViewSet,
    PublicHabitListView,
    HabitCompleteView,
    HabitStatsView,
    UserHabitsListView
)

# Создаем router для ViewSet
router = DefaultRouter()
router.register(r'', HabitViewSet, basename='habit')

# Создаем схему для Swagger/OpenAPI
schema_view = get_schema_view(
    openapi.Info(
        title="Habits API",
        default_version='v1',
        description="API для трекера привычек (Atomic Habits)",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Основные CRUD эндпоинты через ViewSet
    path('', include(router.urls)),

    # Список привычек текущего пользователя (с пагинацией)
    path('my/', UserHabitsListView.as_view(), name='my-habits'),

    # Список публичных привычек
    path('public/', PublicHabitListView.as_view(), name='public-habits'),

    # Отметить выполнение привычки
    path('<int:pk>/complete/', HabitCompleteView.as_view(), name='habit-complete'),

    # Статистика по привычкам
    path('stats/', HabitStatsView.as_view(), name='habit-stats'),

    # Документация API
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]