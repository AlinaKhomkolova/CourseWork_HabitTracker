from django.core.exceptions import ValidationError


def validate_related_habit_and_reward(habit):
    """Проверка, что нельзя заполнять одновременно и связанное действие, и вознаграждение."""
    if habit.related_habit and habit.reward:
        raise ValidationError(
            "Нельзя заполнить одновременно и связанное действие, и вознаграждение. Выберите только одно."
        )
