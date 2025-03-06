from celery import shared_task
from django.utils.timezone import now

from habit.models import Habit
from habit.services import send_telegram_message


@shared_task(bind=True, max_retries=5, default_retry_delay=30)
def send_habit_reminders(self):
    current_time = now().replace(second=0, microsecond=0)
    print(f"Текущее время: {current_time}")
    habits = Habit.objects.filter(time__hour=current_time.hour, time__minute=current_time.minute)
    print(f"Найдено привычек: {habits.count()}")

    if habits.count() == 0:
        print("Нет привычек для напоминания. Ожидание и повторная попытка.")
        raise self.retry(countdown=30)

    for habit in habits:
        user = habit.owner
        print(f"Проверяем пользователя: {user.username}, chat_id: {user.tg_chat_id}")

    if user.tg_chat_id:
        message = f"Напоминание о привычке: {habit.name}"
        print('Отправка')
        send_telegram_message(user.tg_chat_id, message)
