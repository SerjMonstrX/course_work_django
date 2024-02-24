from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

NULLABLE = {'blank': True, 'null': True}


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email address is required')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='почта', unique=True)
    is_active = models.BooleanField(default=True, verbose_name='подтвержден ли аккаунт')
    verification_token = models.CharField(max_length=100, verbose_name='Токен верификации', **NULLABLE)
    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    client_email = models.EmailField(verbose_name='почта клиента')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'

    def __str__(self):
        return self.client_email


class Mailing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, verbose_name='клиенты', **NULLABLE)
    title = models.CharField(max_length=100, verbose_name='название рассылки')
    start_time = models.TimeField(verbose_name='время рассылки',)
    frequency = models.CharField(max_length=20, verbose_name='периодичность',
                                 choices=[('daily', 'Ежедневно'), ('weekly', 'Еженедельно'), ('monthly', 'Ежемесячно')])
    status = models.CharField(max_length=20, verbose_name='статус рассылки',
                              choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена')])

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return self.title  # выводим название рассылки



class Message(models.Model):
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='принадлежность к рассылке')
    subject = models.CharField(max_length=255, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело письма')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class MailingLog(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='тело письма')
    attempt_time = models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')
    status = models.CharField(max_length=20, verbose_name='статус попытки')
    server_response = models.TextField(verbose_name='ответ сервера', **NULLABLE)

    class Meta:
        verbose_name = 'Логи рассылки'
        verbose_name_plural = 'Логи рассылки'
