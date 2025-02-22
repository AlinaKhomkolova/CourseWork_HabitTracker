from django.urls import path

from .views import HabitCreateView, HabitListView, HabitRetrieveAPIView, HabitDestroyAPIView

urlpatterns = [
    # Просмотр всех привычек
    path('habits/', HabitListView.as_view(), name='habit-list'),
    # Создание привычки
    path('habits/create/', HabitCreateView.as_view(), name='habit-create'),
    # Просмотр одной привычки
    path('habits/<int:pk>/', HabitRetrieveAPIView.as_view(), name='habit-retrieve'),
    # Удаление привычки
    path('habits/<int:pk>/delete/', HabitDestroyAPIView.as_view(), name='habit-delete'),
]
