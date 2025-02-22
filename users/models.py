from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

from config.settings import NULLABLE


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """Модель пользователя"""
    first_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пользователя',
        **NULLABLE
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        **NULLABLE
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email пользователя'
    )
    city = models.CharField(
        max_length=150,
        verbose_name='Город проживания пользователя',
        **NULLABLE
    )
    token = models.CharField(
        max_length=100,
        verbose_name='Токен',
        **NULLABLE
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def username(self):
        return self.get_username()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
