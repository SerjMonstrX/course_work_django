from datetime import datetime, timezone

from config.celery import app
from django.core.mail import send_mail, BadHeaderError
from celery_once import QueueOnce

from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, MailingLog


# @app.task(bind=True, ignore_result=True)
# def process_mailing(mailing_id, *args, **kwargs):
#     print(f"Received mailing_id: {mailing_id}")
#     current_datetime = datetime.now(timezone.utc)
#     mailing = Mailing.objects.get(id=mailing_id)
#
#     # Отправляем сообщение каждому клиенту в списке получателей
#     for client in mailing.clients.all():
#         try:
#             print(mailing.get_message_subject())
#             print(mailing.get_message_body())
#             print(EMAIL_HOST_USER)
#             print([client.client_email])
#             send_mail(
#                 subject=mailing.get_message_subject(),
#                 message=mailing.get_message_body(),
#                 # from_email=mailing.user.email(),
#                 from_email=EMAIL_HOST_USER,
#                 recipient_list=[client.client_email],
#             )
#             # Создаем запись в логах рассылки при успешной отправке
#             MailingLog.objects.create(
#                 mailing=mailing,
#                 client=client,
#                 attempt_time=current_datetime,
#                 status='success',
#                 server_response='Mail sent successfully'
#             )
#         except BadHeaderError as e:
#             # Создаем запись в логах рассылки при ошибке отправки
#             MailingLog.objects.create(
#                 mailing=mailing,
#                 client=client,
#                 attempt_time=current_datetime,
#                 status='error',
#                 server_response=str(e)
#             )
#         except Exception as e:
#             # Обработка других ошибок при отправке сообщения
#             # создаем запись в логах рассылки
#             MailingLog.objects.create(
#                 mailing=mailing,
#                 client=client,
#                 attempt_time=current_datetime,
#                 status='error',
#                 server_response=str(e)
#             )


@app.task()
def start_mailing():
    # Получаем все объекты Mailing из базы данных
    mailings = Mailing.objects.all()

    # Перебираем каждый объект Mailing
    for mailing in mailings:
        # Проверяем статус рассылки
        if mailing.status not in ['created', 'started']:
            # Если статус не является 'created' или 'started', переходим к следующему объекту
            continue

        # Получаем текущее время и дату
        current_datetime = datetime.now(timezone.utc)

        # Проверяем, наступила ли дата начала рассылки
        if current_datetime.date() >= mailing.start_date:
            # Проверяем, не наступила ли дата окончания рассылки
            if current_datetime.date() <= mailing.end_date:
                # Проверяем, наступило ли время начала рассылки
                if mailing.start_time is None or current_datetime.time() >= mailing.start_time:
                    # Если все условия выполнены, обновляем статус рассылки на 'started'
                    mailing.status = 'started'
                    mailing.save()

                    for client in mailing.clients.all():
                        try:
                            message_subject = mailing.get_message_subject()
                            message_body = mailing.get_message_body()
                            send_mail(
                                subject=message_subject,
                                message=message_body,
                                from_email=EMAIL_HOST_USER,
                                recipient_list=[client.client_email],
                            )
                            # Создаем запись в логах рассылки при успешной отправке
                            MailingLog.objects.create(
                                message=mailing.message_set.first(),
                                attempt_time=current_datetime,
                                status='success',
                                server_response='Mail sent successfully',
                            )
                        except BadHeaderError as e:
                            # Создаем запись в логах рассылки при ошибке отправки
                            MailingLog.objects.create(
                                message=mailing.message_set.first(),
                                attempt_time=current_datetime,
                                status='error',
                                server_response=str(e),
                            )
                        except Exception as e:
                            # Обработка других ошибок при отправке сообщения
                            # создаем запись в логах рассылки
                            MailingLog.objects.create(
                                message=mailing.message_set.first(),
                                attempt_time=current_datetime,
                                status='error',
                                server_response=str(e),
                            )