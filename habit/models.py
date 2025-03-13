from django.db import models

from config.settings import NULLABLE
from habit.validation import validate_related_habit_and_reward, validate_time_to_complete, \
    validate_related_habit_is_pleasant, validate_frequency_max_7_days, validate_frequency_min_7_days, \
    validate_pleasant_habit
from users.models import User


class Habit(models.Model):
    # Пользователь — создатель привычки
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='habits',
        verbose_name='Создатель привычки'
    )

    name = models.CharField(
        max_length=250,
        verbose_name='Название привычки'
    )
    place = models.CharField(
        max_length=255,
        verbose_name='Место выполнения привычки',
        **NULLABLE
    )
    time = models.TimeField(
        verbose_name='Время, когда необходимо выполнять привычку.'
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Описание действия'
    )
    # Полезная=False, Приятная=True
    is_pleasant_habit = models.BooleanField(
        default=False,
        verbose_name='Является ли привычка приятной'
    )
    # Связанная привычка (для полезных привычек)
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='related_habits',
        **NULLABLE,
    )
    frequency = models.IntegerField(
        default=1,
        verbose_name='Периодичность(Сколько раз в неделю)'
    )
    last_completed_frequency = models.DateTimeField(
        verbose_name='Дата последнего выполнения привычки',
        **NULLABLE
    )

    reward = models.CharField(
        max_length=255,
        verbose_name='Вознаграждение',
        **NULLABLE
    )
    time_to_complete = models.DurationField(
        verbose_name='Время на выполнение привычки',
    )
    # Булевое поле, которое позволяет сделать привычку публичной.
    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичность привычки'
    )

    def clean(self):
        validate_related_habit_and_reward(self)
        validate_time_to_complete(self)
        validate_related_habit_is_pleasant(self)
        validate_pleasant_habit(self)
        validate_frequency_min_7_days(self)
        validate_frequency_max_7_days(self)

    def __str__(self):
        return self.name
