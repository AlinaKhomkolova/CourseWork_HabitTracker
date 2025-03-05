from datetime import timedelta

import django
from django.core.exceptions import ValidationError
from django.utils import timezone

django.setup()
from django.apps import apps


def validate_related_habit_and_reward(habit):
    """Проверка, что нельзя заполнять одновременно и связанную привычку, и вознаграждение."""
    if habit.related_habit and habit.reward:
        raise ValidationError(
            'Нельзя заполнить одновременно и связанную привычку, и вознаграждение. Выберите только одно.'
        )


def validate_time_to_complete(value):
    """
    Валидатор, проверяющий, что время выполнения привычки не больше 120 секунд (2 минуты).
    """
    if value.time_to_complete > timedelta(seconds=120):
        raise ValidationError('Время выполнения привычки не должно превышать 120 секунд (2 минуты).')


def validate_related_habit_is_pleasant(value):
    """
    Валидатор, который проверяет, что связанная привычка является приятной.
    """
    Habit = apps.get_model('habit', 'Habit')

    if value.related_habit:  # Если есть связанная привычка
        related_habit = Habit.objects.filter(id=value.related_habit.id).first()
        if related_habit and not related_habit.is_pleasant_habit:
            raise ValidationError('Связанная привычка должна быть приятной.')


def validate_pleasant_habit(habit):
    """Проверка, что у приятной привычки нет вознаграждения или связанной привычки."""
    if habit.is_pleasant_habit:
        if habit.reward:
            raise ValidationError('У приятной привычки не может быть вознаграждения.')
        if habit.related_habit:
            raise ValidationError('У приятной привычки не может быть связанной привычки.')


def validate_frequency_min_7_days(habit):
    """Проверка, что привычка выполняется хотя бы 1 раз в 7 дней."""
    if habit.frequency < 1:
        raise ValidationError('Периодичность привычки должна быть не реже 1 раза в 7 дней.')
    if habit.frequency > 7:
        raise ValidationError('Периодичность привычки должна быть больше 7 раз в 7 дней.')



def validate_frequency_max_7_days(habit):
    """Проверка, что привычку нельзя не выполнять более 7 дней."""
    if habit.last_completed_frequency:
        days_since_last = timezone.now() - habit.last_completed_frequency
        if days_since_last > timedelta(days=7):
            raise ValidationError('Нельзя не выполнять привычку более 7 дней.')
