from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User"""

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])  # Хэшируем пароль
        return super().create(validated_data)


