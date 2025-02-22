from django.db import models

from config.settings import NULLABLE
from users.models import User


# Create your models here.
class Habit(models.Model):
    HABIT_TYPE_CHOICES = [
        ('Полезная', 'Полезная'),
        ('Приятная', 'Приятная'),
    ]

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
    habit_type = models.CharField(
        max_length=10,
        choices=HABIT_TYPE_CHOICES,
        default='Полезная',
        verbose_name='Тип привычки'
    )
    place = models.CharField(
        max_length=255,
        verbose_name='Место выполнения привычки',
        **NULLABLE
    )
    time = models.TimeField(
        verbose_name='Время выполнения привычки'
    )
    action = models.CharField(
        max_length=255,
        verbose_name='Описание действия'
    )
    is_pleasant_habit = models.BooleanField(
        default=False,
        verbose_name='Является ли привычка приятной'
    )
    # Связанная привычка (для полезных привычек)
    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='related_habits',
        **NULLABLE
    )
    frequency = models.CharField(
        max_length=50,
        default='Ежедневно',
        verbose_name='Периодичность'
    )
    reward = models.CharField(
        max_length=255,
        verbose_name='Вознаграждение'
    )
    time_to_complete = models.DurationField(
        verbose_name='Время на выполнение привычки'
    )
    # Булевое поле, которое позволяет сделать привычку публичной.
    is_public = models.BooleanField(
        default=False,
        verbose_name='Публичность привычки'
    )

    def __str__(self):
        return self.name
