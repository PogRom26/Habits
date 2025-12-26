import requests
from django.conf import settings
from celery import shared_task


class TelegramBot:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.api_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, chat_id, text):
        url = f"{self.api_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=data)
        return response.json()


@shared_task
def send_habit_reminder(habit_id, user_telegram_id):
    from habits.models import Habit
    from django.utils import timezone

    try:
        habit = Habit.objects.get(id=habit_id)
        bot = TelegramBot()

        message = f"⏰ Напоминание о привычке!\n\n"
        message += f"📍 Место: {habit.place}\n"
        message += f"⏰ Время: {habit.time.strftime('%H:%M')}\n"
        message += f"🎯 Действие: {habit.action}\n"
        message += f"⏱ Длительность: {habit.duration} секунд"

        if habit.reward:
            message += f"\n🎁 Вознаграждение: {habit.reward}"

        bot.send_message(user_telegram_id, message)

        # Обновляем время последнего напоминания
        habit.last_reminder = timezone.now()
        habit.save()

    except Habit.DoesNotExist:
        pass