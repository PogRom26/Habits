from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Habit
from telegram.services import send_habit_reminder


@shared_task
def check_and_send_reminders():
    """Проверка и отправка напоминаний о привычках"""
    now = timezone.now()
    current_time = now.time()

    # Получаем привычки, для которых нужно отправить напоминание
    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    ).select_related('user')

    for habit in habits:
        # Проверяем, отправлялось ли уже напоминание сегодня
        if habit.last_reminder and habit.last_reminder.date() == now.date():
            continue

        # Проверяем периодичность
        days_passed = (now.date() - habit.created_at.date()).days
        if days_passed % habit.periodicity == 0:
            # Отправляем напоминание через задачу
            if habit.user.telegram_id:
                send_habit_reminder.delay(habit.id, habit.user.telegram_id)