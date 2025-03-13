from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery

# Установка переменной окружения для настроек проекта os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_project.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# Создание экземпляра объекта Celery`
app = Celery('config')

# Загрузка настроек из файла Django`
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django`
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        timedelta(seconds=1),  # Запуск каждую секунду
        'habit.tasks.send_habit_reminders',
        name='Проверка каждую секунду'
    )
