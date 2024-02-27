from config.celery import app
from django.core.mail import send_mail
from celery_once import QueueOnce


@app.task(base=QueueOnce)
def mail_process():
    send_mail(
        subject="test1",
        message='hello',
        from_email='cosmusbz@mail.ru',
        recipient_list=['cosmusbz@mail.ru', 'sss@ss.ru']  # Изменил множество на список
    )