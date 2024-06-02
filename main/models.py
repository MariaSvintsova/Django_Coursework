from django.db import models

from config import settings
from users.models import User

NULLABLE = {'blank': True, 'null': True}

class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name='Фамилия, Имя, Отчество')
    email = models.EmailField(unique=True, verbose_name='Контактный email')
    message = models.TextField(verbose_name='Комментарий', **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return self.name

class Message(models.Model):
    title = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(max_length=255, verbose_name='Тело письма')

    class Meta:
        verbose_name = 'Сообщение для рассылки'
        verbose_name_plural = 'Сообщения для рассылок'

    def __str__(self):
        return self.title


class NewsLetter(models.Model):
    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    FREQUENCY = [
        (DAILY, 'Раз в день'),
        (WEEKLY, 'Раз в неделю'),
        (MONTHLY, 'Раз в месяц')
    ]

    CREATED = 'created'
    LAUNCHED = 'launched'
    COMPLETED = 'completed'

    STATUS_CHOICES = [
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена'),
        (COMPLETED, 'Завершена')
    ]

    is_published = models.BooleanField(default=True, verbose_name='Опубликован')
    create_time = models.TimeField(auto_now_add=True, verbose_name='Время рассылки')
    create_date = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    frequency = models.CharField(max_length=10, choices=FREQUENCY, verbose_name='Периодичность')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    message = models.OneToOneField(Message, on_delete=models.CASCADE, verbose_name='Сообщение', **NULLABLE)
    client = models.ManyToManyField(Client,  verbose_name='Клиент', **NULLABLE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE)


    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f'Рассылка {self.pk}'


class SendAttemp(models.Model):
    SUCCESS = 'success'
    FAILURE = 'failure'

    STATUS_CHOICES = [
        (SUCCESS, 'Успешно'),
        (FAILURE, 'Неуспешно'),
    ]

    newsletter = models.ForeignKey(NewsLetter, on_delete=models.CASCADE, related_name='send_attempts', verbose_name='Рассылка')
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время отправки')
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, verbose_name='Статус попытки')
    server_response = models.TextField(**NULLABLE, verbose_name='Ответ сервера')

    class Meta:
        verbose_name = 'Попытка отправки письма'
        verbose_name_plural = 'Попытки отправки письма'

    def __str__(self):
        return f'Попытка {self.pk}'
