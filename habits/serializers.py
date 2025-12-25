# habits/serializers.py
from rest_framework import serializers
from django.utils import timezone
from .models import Habit, HabitCompletion
from .validators import HabitValidator


class HabitSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для привычки"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Habit
        fields = [
            'id', 'user', 'user_email', 'place', 'time', 'action',
            'is_pleasant', 'related_habit', 'periodicity', 'reward',
            'duration', 'is_public', 'created_at', 'is_owner'
        ]
        read_only_fields = ('user', 'created_at')

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request:
            return obj.user == request.user
        return False

    def validate(self, data):
        validator = HabitValidator()

        # Проверка на вознаграждение или связанную привычку
        validator.validate_reward_or_related_habit(data)

        # Проверка приятной привычки
        validator.validate_pleasant_habit(data)

        # Проверка периодичности
        if 'periodicity' in data:
            validator.validate_periodicity(data['periodicity'])

        # Проверка времени выполнения
        if 'duration' in data:
            validator.validate_duration(data['duration'])

        # Проверка связанной привычки
        related_habit = data.get('related_habit')
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                'Связанная привычка должна быть приятной.'
            )

        return data


class HabitCreateSerializer(HabitSerializer):
    """Сериализатор для создания привычки"""

    class Meta(HabitSerializer.Meta):
        fields = HabitSerializer.Meta.fields


class HabitDetailSerializer(HabitSerializer):
    """Сериализатор для детального просмотра привычки"""
    related_habit_info = serializers.SerializerMethodField()
    completions_count = serializers.SerializerMethodField()

    class Meta(HabitSerializer.Meta):
        fields = HabitSerializer.Meta.fields + ['related_habit_info', 'completions_count']

    def get_related_habit_info(self, obj):
        if obj.related_habit:
            return {
                'id': obj.related_habit.id,
                'action': obj.related_habit.action,
                'duration': obj.related_habit.duration
            }
        return None

    def get_completions_count(self, obj):
        return HabitCompletion.objects.filter(habit=obj).count()


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор для публичных привычек"""
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Habit
        fields = [
            'id', 'user_email', 'place', 'time', 'action',
            'duration', 'is_public', 'created_at'
        ]
        read_only_fields = fields


class HabitCompletionSerializer(serializers.ModelSerializer):
    """Сериализатор для отметок о выполнении привычки"""
    habit_action = serializers.CharField(source='habit.action', read_only=True)

    class Meta:
        model = HabitCompletion
        fields = ['id', 'habit', 'habit_action', 'completed_at', 'was_successful']
        read_only_fields = ['completed_at']


class HabitStatsSerializer(serializers.Serializer):
    """Сериализатор для статистики"""
    total_habits = serializers.IntegerField()
    completed_today = serializers.IntegerField()
    completed_this_week = serializers.IntegerField()
    success_rate = serializers.FloatField()
    public_habits = serializers.IntegerField()
    pleasant_habits = serializers.IntegerField()