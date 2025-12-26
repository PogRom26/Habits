# habits/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Habit(models.Model):
    PERIOD_CHOICES = [
        (1, 'Ежедневно'),
        (2, 'Раз в 2 дня'),
        (3, 'Раз в 3 дня'),
        (4, 'Раз в 4 дня'),
        (5, 'Раз в 5 дней'),
        (6, 'Раз в 6 дней'),
        (7, 'Раз в неделю'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='habits'
    )

    place = models.CharField(
        max_length=255,
        verbose_name='Место выполнения'
    )

    time = models.TimeField(verbose_name='Время выполнения')

    action = models.CharField(
        max_length=500,
        verbose_name='Действие'
    )

    is_pleasant = models.BooleanField(
        default=False,
        verbose_name='Признак приятной привычки'
    )

    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Связанная привычка',
        related_name='related_to'
    )

    periodicity = models.PositiveSmallIntegerField(
        choices=PERIOD_CHOICES,
        default=1,
        verbose_name='Периодичность (в днях)'
    )

    reward = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Вознаграждение'
    )

    duration = models.PositiveSmallIntegerField(
        verbose_name='Время на выполнение (в секундах)',
        validators=[MinValueValidator(1), MaxValueValidator(120)]
    )

    is_public = models.BooleanField(
        default=False,
        verbose_name='Признак публичности'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    last_reminder = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Последнее напоминание'
    )

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ['time']

    def __str__(self):
        return f"{self.action} в {self.time} ({self.user.username})"


class HabitCompletion(models.Model):
    """Отметки о выполнении привычек"""
    habit = models.ForeignKey(
        Habit,
        on_delete=models.CASCADE,
        related_name='completions',
        verbose_name='Привычка'
    )
    completed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата и время выполнения'
    )
    was_successful = models.BooleanField(
        default=True,
        verbose_name='Успешно выполнено'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Заметки'
    )

    class Meta:
        verbose_name = 'Выполнение привычки'
        verbose_name_plural = 'Выполнения привычек'
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.habit.action} выполнена {self.completed_at}"