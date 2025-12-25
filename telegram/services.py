# telegram_service/services.py
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class TelegramBot:
    def __init__(self):
        self.token = settings.TELEGRAM_BOT_TOKEN
        self.api_url = f"https://api.telegram.org/bot{self.token}"

    def send_message(self, chat_id, text, parse_mode='HTML'):
        """Отправка сообщения в Telegram"""
        if not self.token:
            logger.error("TELEGRAM_BOT_TOKEN не настроен в settings.py")
            return False

        if not chat_id:
            logger.error("Chat ID не указан")
            return False

        try:
            url = f"{self.api_url}/sendMessage"
            data = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode,
                "disable_web_page_preview": True
            }

            response = requests.post(url, json=data, timeout=10)
            response.raise_for_status()

            logger.info(f"Сообщение отправлено в Telegram chat_id: {chat_id}")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при отправке в Telegram: {e}")
            return False

    def get_bot_info(self):
        """Получение информации о боте"""
        try:
            url = f"{self.api_url}/getMe"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении информации о боте: {e}")
            return None


# Создаем глобальный экземпляр бота
telegram_bot = TelegramBot()