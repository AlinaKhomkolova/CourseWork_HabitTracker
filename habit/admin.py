from django.contrib import admin

from habit.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'place', 'time', 'action', 'is_pleasant_habit', 'related_habit', 'frequency',
                    'last_completed_frequency', 'reward', 'time_to_complete', 'is_public')
    search_fields = ('id', 'owner')
    list_filter = ('time',)
