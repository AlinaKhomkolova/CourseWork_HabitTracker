from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Habit
from .permissions import IsOwnerOrStaff
from .serializers import HabitSerializer


class HabitCreateView(generics.CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        При создании урока автоматически назначает владельца текущего пользователя
        """
        serializer.save(owner=self.request.user)


class HabitListView(generics.ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращает список привычек:
         - Если пользователь — администратор, он видит все привычки.
        - Если обычный пользователь, он видит только свои привычки и публичные
        """
        user = self.request.user
        if user.is_staff:
            return Habit.objects.all()
        return Habit.objects.filter(owner=user) | Habit.objects.filer(is_public=True)


class HabitRetrieveAPIView(generics.RetrieveAPIView):
    """
    API для получения одной привычки.
    Доступ:
    - Только владелец привычки или администратор.
    Метод:
    - `retrieve()`
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrStaff]


class HabitUpdateAPIView(generics.UpdateAPIView):
    """
    API для обновления привычки.
    Доступ:
    - Только владелец привычки или администратор.
    Метод:
    - `update()`
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrStaff]


class HabitDestroyAPIView(generics.DestroyAPIView):
    """
    API для удаления привычки.
    Доступ:
    - Только владелец привычки или администратор.
    Метод:
    - `destroy()`
    """
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrStaff]
