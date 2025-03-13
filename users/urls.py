from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import RegisterView, UserViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(f'users', UserViewSet, basename='users')

urlpatterns = [
    # Регистрация маршрута для API, чтобы получить доступ к данным пользователя
    path('api/', include(router.urls)),

    # Эндпоинт для регистрации пользователя
    path('register/', RegisterView.as_view(), name='register'),

    # Эндпоинт для получения JWT-токена
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Эндпоинт для обновления JWT-токена
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
