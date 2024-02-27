from django.contrib.auth import get_user_model
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    client_email = models.EmailField(verbose_name='почта клиента')
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)

    class Meta:
        verbose_name = 'Клиент сервиса'
        verbose_name_plural = 'Клиенты сервиса'

    def __str__(self):
        return self.client_email


class Mailing(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client, verbose_name='клиенты', **NULLABLE)
    title = models.CharField(max_length=100, verbose_name='название рассылки')
    start_time = models.TimeField(verbose_name='время рассылки', **NULLABLE)
    start_date = models.DateField(verbose_name='время рассылки', **NULLABLE)
    end_date = models.DateField(verbose_name='время рассылки', **NULLABLE)
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
