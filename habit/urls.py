from django.urls import path

from .apps import HabitConfig
from .views import HabitCreateView, HabitListView, HabitRetrieveAPIView, HabitDestroyAPIView, HabitUpdateAPIView

app_name = HabitConfig.name

urlpatterns = [
    # Просмотр всех привычек
    path('habits/', HabitListView.as_view(), name='habit-list'),
    # Создание привычки
    path('habits/create/', HabitCreateView.as_view(), name='habit-create'),
    # Просмотр одной привычки
    path('habits/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit-retrieve'),
    # Редактирование привычки
    path('habits/<int:pk>/update', HabitUpdateAPIView.as_view(), name='habit-update'),
    # Удаление привычки
    path('habits/<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='habit-delete', ),
]
