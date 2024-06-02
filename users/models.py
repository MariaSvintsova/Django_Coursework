from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}

class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')
    message = models.TextField(verbose_name='Комментарий',  **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# Добавление или изменение related_name для поля groups
User.groups.field.remote_field.related_name = 'custom_user_groups'

# Добавление или изменение related_name для поля user_permissions
User.user_permissions.field.remote_field.related_name = 'custom_user_permissions'
