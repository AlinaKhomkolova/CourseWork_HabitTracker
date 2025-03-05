from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTest(TestCase):

    def test_create_user(self):
        """Проверка, что пользователь создается корректно"""
        user = get_user_model().objects.create_user(
            email="testuser@mail.com",
            password="password123",
            first_name="John",
            last_name="Doe"
        )
        self.assertEqual(user.email, "testuser@mail.com")
        self.assertTrue(user.check_password("password123"))

    def test_create_user_without_email(self):
        """Проверка, что нельзя создать пользователя без email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="password123"
            )

    def test_create_superuser_without_email(self):
        """Проверка, что нельзя создать суперпользователя без email"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email=None,
                password="password123"
            )
