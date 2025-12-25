# habits/views.py
from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from .models import Habit, HabitCompletion
from .serializers import (
    HabitSerializer,
    HabitCreateSerializer,
    HabitDetailSerializer,
    PublicHabitSerializer,
    HabitCompletionSerializer,
    HabitStatsSerializer
)
from .permissions import IsOwnerOrReadOnly
from .validators import HabitValidator


class HabitPagination(PageNumberPagination):
    """Пагинация по 5 привычек на страницу"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class HabitViewSet(viewsets.ModelViewSet):
    """ViewSet для управления привычками (CRUD)"""
    queryset = Habit.objects.all()
    pagination_class = HabitPagination
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_pleasant', 'is_public']

    def get_serializer_class(self):
        if self.action == 'create':
            return HabitCreateSerializer
        elif self.action == 'retrieve':
            return HabitDetailSerializer
        return HabitSerializer

    def get_queryset(self):
        """Возвращаем только привычки текущего пользователя"""
        if self.action == 'list':
            return Habit.objects.filter(user=self.request.user)
        return super().get_queryset()

    def perform_create(self, serializer):
        """При создании привычки назначаем текущего пользователя"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def pleasant(self, request):
        """Список приятных привычек пользователя"""
        habits = Habit.objects.filter(
            user=request.user,
            is_pleasant=True
        )
        page = self.paginate_queryset(habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(habits, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Привычки на сегодня"""
        today_habits = Habit.objects.filter(
            user=request.user
        ).order_by('time')

        page = self.paginate_queryset(today_habits)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(today_habits, many=True)
        return Response(serializer.data)


class UserHabitsListView(generics.ListAPIView):
    """Список привычек текущего пользователя"""
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user).order_by('time')


class PublicHabitListView(generics.ListAPIView):
    """Список публичных привычек (доступно всем)"""
    serializer_class = PublicHabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by('-created_at')


class HabitCompleteView(APIView):
    """Отметить выполнение привычки"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            habit = Habit.objects.get(pk=pk, user=request.user)
        except Habit.DoesNotExist:
            return Response(
                {'error': 'Привычка не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Создаем запись о выполнении
        completion = HabitCompletion.objects.create(
            habit=habit,
            was_successful=True
        )

        serializer = HabitCompletionSerializer(completion)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class HabitStatsView(APIView):
    """Статистика по привычкам пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        habits = Habit.objects.filter(user=user)

        # Рассчитываем статистику
        total_habits = habits.count()
        completed_today = HabitCompletion.objects.filter(
            habit__user=user,
            completed_at__date=timezone.now().date()
        ).count()

        # Привычки на этой неделе
        week_start = timezone.now() - timedelta(days=timezone.now().weekday())
        habits_this_week = HabitCompletion.objects.filter(
            habit__user=user,
            completed_at__gte=week_start
        ).count()

        # Процент успешных выполнений
        total_completions = HabitCompletion.objects.filter(habit__user=user).count()
        successful_completions = HabitCompletion.objects.filter(
            habit__user=user,
            was_successful=True
        ).count()

        success_rate = (successful_completions / total_completions * 100) if total_completions > 0 else 0

        stats = {
            'total_habits': total_habits,
            'completed_today': completed_today,
            'completed_this_week': habits_this_week,
            'success_rate': round(success_rate, 1),
            'public_habits': habits.filter(is_public=True).count(),
            'pleasant_habits': habits.filter(is_pleasant=True).count(),
        }

        return Response(stats)