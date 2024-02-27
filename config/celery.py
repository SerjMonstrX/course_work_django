import os
from celery import Celery
from celery_once import QueueOnce
from django.core.mail import send_mail
from config import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.conf.ONCE = settings.CELERY_ONCE  # force CELERY_ONCE to load settings
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

#
# celery = Celery('tasks', broker='amqp://guest@localhost//')
# celery.conf.ONCE = {
#   'backend': 'celery_once.backends.Redis',
#   'settings': {
#     'url': 'redis://127.0.0.1:6379/0',
#     'default_timeout': 60 * 60
#   }
# }
#
# @app.task(base=QueueOnce, once={'graceful': True})
# def mail_process():
#     send_mail(
#         subject="test1",
#         message='hello',
#         from_email='cosmusbz@mail.ru',
#         recipient_list=['cosmusbz@mail.ru', 'sss@ss.ru',] # recipient_list должен быть списком строк
#     )
