from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework.test import APITestCase

from habit.models import Habit
from habit.validation import validate_time_to_complete, validate_related_habit_is_pleasant, validate_pleasant_habit, \
    validate_frequency_max_7_days, validate_frequency_min_7_days
from users.models import User


class HabitValidatorTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='alina@fob.ru', password='Poma2404')
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            owner=self.user,
            name="Test Habit",
            time_to_complete=timedelta(seconds=90),
            action="Action",
            is_pleasant_habit=True,
            time=timezone.now()
        )

    def test_validate_related_habit_and_reward(self):
        """Тестирование валидатора, который проверяет, что нельзя заполнить одновременно связанную привычку и вознаграждение"""
        # Привычка с вознаграждением и связанной привычкой
        self.habit.reward = "Шоколад"
        self.habit.related_habit = self.habit  # Связали с самой собой

        with self.assertRaises(ValidationError) as context:
            self.habit.full_clean()

        self.assertIn(
            'Нельзя заполнить одновременно и связанную привычку, и вознаграждение. Выберите только одно.',
            context.exception.message_dict['__all__']
        )

    def test_validate_time_to_complete(self):
        """Тестирование валидатора времени выполнения привычки"""
        data = Habit.objects.create(
            owner=self.user,
            name="Test Habit",
            time_to_complete=timedelta(seconds=130),  # Больше 120 секунд
            action="Action",
            is_pleasant_habit=True,
            time=timezone.now()
        )
        with self.assertRaises(ValidationError) as context:
            validate_time_to_complete(data)

            self.assertIn(
                'Время выполнения привычки не должно превышать 120 секунд (2 минуты).',
                context.exception.message_dict['__all__']
            )

    def test_validate_related_habit_is_pleasant(self):
        """Тестирование валидатора, который проверяет, что связанная привычка должна быть приятной"""
        pleasant_habit = Habit.objects.create(owner=self.user,
                                              name="Pleasant Habit",
                                              is_pleasant_habit=True,
                                              time_to_complete=timedelta(seconds=60),
                                              action="Action",
                                              time=timezone.now())
        unpleasant_habit = Habit.objects.create(owner=self.user,
                                                name="Unpleasant Habit",
                                                is_pleasant_habit=False,
                                                time_to_complete=timedelta(seconds=60),
                                                action="Action",
                                                time=timezone.now())

        habit = Habit(owner=self.user,
                      name="Test Habit",
                      related_habit=unpleasant_habit,
                      time_to_complete=timedelta(seconds=60),
                      action="Action",
                      time=timezone.now())

        with self.assertRaises(ValidationError) as context:
            validate_related_habit_is_pleasant(habit)
        self.assertIn(
            'Связанная привычка должна быть приятной.',
            context.exception)

    def test_validate_pleasant_habit(self):
        """Тестирование валидатора для приятной привычки"""
        pleasant_habit = Habit.objects.create(owner=self.user,
                                              name="Pleasant Habit",
                                              is_pleasant_habit=True,
                                              time_to_complete=timedelta(seconds=60),
                                              action="Action",
                                              time=timezone.now())
        habit = Habit(owner=self.user,
                      name="Pleasant Habit",
                      is_pleasant_habit=True,
                      time_to_complete=timedelta(seconds=60),
                      action="Action",
                      related_habit=pleasant_habit,
                      reward='Шоколад',
                      time=timezone.now()
                      )
        with self.assertRaises(ValidationError) as context:
            validate_pleasant_habit(habit)
            self.assertIn(
                'У приятной привычки не может быть вознаграждения.',
                context.exception)
        with self.assertRaises(ValidationError) as context:
            validate_pleasant_habit(habit)
            self.assertIn(
                'У приятной привычки не может быть связанной привычки.',
                context.exception)

    def test_validate_frequency_min_7_days(self):
        """Тестирование валидатора для минимальной частоты выполнения привычки"""
        habit_min = Habit(owner=self.user,
                          name="Test Habit",
                          frequency=0,
                          time_to_complete=timedelta(seconds=60),
                          action="Action",
                          time=timezone.now()
                          )
        habit_max = Habit(owner=self.user,
                          name="Test Habit",
                          frequency=0,
                          time_to_complete=timedelta(seconds=60),
                          action="Action",
                          time=timezone.now()
                          )
        with self.assertRaises(ValidationError) as context:
            validate_frequency_min_7_days(habit_min)
            self.assertIn(
                'Периодичность привычки должна быть не реже 1 раза в 7 дней.',
                context.exception)
        with self.assertRaises(ValidationError) as context:
            validate_frequency_min_7_days(habit_max)
            self.assertIn(
                'Периодичность привычки должна быть не реже 1 раза в 7 дней.',
                context.exception)

    def test_validate_frequency_max_7_days(self):
        habit = Habit(owner=self.user,
                      name="Test Habit",
                      last_completed_frequency=timezone.now() - timedelta(days=8),
                      time_to_complete=timedelta(seconds=60),
                      action="Action",
                      time=timezone.now()
                      )
        with self.assertRaises(ValidationError) as context:
            validate_frequency_max_7_days(habit)
            self.assertIn(
                'Нельзя не выполнять привычку более 7 дней.',
                context.exception)
