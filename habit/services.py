import requests

from config import settings


def send_telegram_message(chat_id, message):
    params = {
        'text': message,
        'chat_id': chat_id,
    }
    requests.get(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage', params=params)
