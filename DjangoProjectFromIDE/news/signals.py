import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import News


@receiver(post_save, sender=News)
def send_news_to_telegram(sender, instance, created, **kwargs):
    """
    Сигнал срабатывает при сохранении новости.
    created = True, если это создание новой записи (а не редактирование старой).
    """
    # Проверяем, что новость только что создана И имеет статус "Опубликовано"
    # (Если у тебя Status не TextChoices, замени instance.Status.PUBLISHED на 'PB')
    if created:

        # Собираем текст сообщения
        message = (
            f"📌 **Нова публікація!**\n\n"
            f"🔥 *{instance.title}*\n\n"
            f"✍️ Автор: {instance.created_by.username}\n"
            f"📅 Дата: {instance.created_at.strftime('%d.%m.%Y %H:%M')}"
        )

        # URL для отправки запроса в Telegram API
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": settings.TELEGRAM_GROUP_ID,
            "text": message,
            "parse_mode": "Markdown"  # Чтобы работал жирный и курсивный текст
        }

        try:
            # Отправляем запрос, ставим таймаут, чтобы сайт не завис, если Telegram упадет
            response = requests.post(url, json=payload, timeout=5)
            response.raise_for_status()
        except requests.RequestException as e:
            # В реальном проекте тут лучше писать в логи
            print(f"Помилка надсилання новості в Telegram: {e}")