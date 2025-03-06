from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from habit.paginators import MaterialsPagination
from users.models import User
from users.serializers import UserSerializer


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    """
        Представление для работы с пользователями.

        Обрабатывает запросы на создание, чтение, обновление и удаление данных пользователя.
        Доступ только для аутентифицированных пользователей. В качестве фильтрации используется
        только информация о текущем пользователе.
        """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # Ограничение, чтобы выводились только данный для текущего пользователя
    permission_classes = [IsAuthenticated]
    pagination_class = MaterialsPagination

    def get_queryset(self):
        """
        Возвращает только текущего пользователя в качестве queryset.

        Это используется для ограничения доступа к данным только для аутентифицированного пользователя.
        """
        return User.objects.filter(id=self.request.user.id)


class RegisterView(APIView):
    """
    Представление для регистрации нового пользователя.
    Это представление позволяет создать нового пользователя в системе. Доступ без аутентификации.
    """
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        """
        Обрабатывает POST-запрос для регистрации нового пользователя.

        Данные пользователя проходят валидацию через сериализатор `UserSerializer`.
        При успешной валидации, создается новый пользователь и возвращается успешный ответ.
        При неудаче возвращаются ошибки валидации.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
