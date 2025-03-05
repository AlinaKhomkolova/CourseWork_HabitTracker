from rest_framework import serializers
from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        habit = Habit(**data)
        habit.clean()  # Вызовем кастомную валидацию для этой привычки
        return data