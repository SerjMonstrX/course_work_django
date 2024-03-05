from datetime import datetime, timezone, timedelta
from config.celery import app
from django.core.mail import send_mail, BadHeaderError
from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, MailingLog
from django.db.models import Q


@app.task()
def start_mailing():
    mailings = Mailing.objects.filter(Q(status='created') | Q(status='started'))
    print('0', mailings)
    current_datetime = datetime.now(timezone.utc)

    for mailing in mailings:
        # Если дата начала рассылки еще не наступила, пропускаем эту рассылку
        print('1', mailing.title)
        if current_datetime.date() < mailing.start_date:
            continue

        # Если дата окончания рассылки уже наступила, то меняем статус и завершаем рассылку.
        if current_datetime.date() > mailing.end_date:
            print('2', mailing.title)
            mailing.status = 'completed'
            mailing.save()
            continue

        # Проверяем наступила ли дата следующей отправки
        if mailing.next_send < current_datetime.date() and mailing.start_time < current_datetime.time():
            print('3', mailing.title)
            #Отправляем письмо всем участникам рассылки
            for client in mailing.clients.all():
                try:
                    message_subject = mailing.message.subject
                    message_body = mailing.message.body
                    send_mail(
                        subject=message_subject,
                        message=message_body,
                        from_email=EMAIL_HOST_USER,
                        recipient_list=[client.client_email],
                    )
                    # Создаем запись в логах рассылки при успешной отправке
                    MailingLog.objects.create(
                        message=mailing.message,
                        attempt_time=current_datetime,
                        status='success',
                        server_response='Mail sent successfully',
                    )
                    print('4', mailing.title)

                    # Вычисляем время следующей отправки в соответствии с периодичностью
                    if mailing.frequency == 'daily':
                        mailing.next_send = current_datetime.date() + timedelta(days=1)
                        mailing.status = 'started'
                        mailing.save()
                    elif mailing.frequency == 'weekly':
                        mailing.next_send = current_datetime.date() + timedelta(weeks=1)
                        mailing.status = 'started'
                        mailing.save()
                    elif mailing.frequency == 'monthly':
                        mailing.next_send = current_datetime.date() + timedelta(days=30)
                        mailing.status = 'started'
                        mailing.save()



                except BadHeaderError as e:
                    # Создаем запись в логах рассылки при ошибке отправки
                    MailingLog.objects.create(
                        message=mailing.message,
                        attempt_time=current_datetime,
                        status='error',
                        server_response=str(e),
                    )
                except Exception as e:
                    # Обработка других ошибок при отправке сообщения
                    # создаем запись в логах рассылки
                    MailingLog.objects.create(
                        message=mailing.message,
                        attempt_time=current_datetime,
                        status='error',
                        server_response=str(e),
                    )


def send_mailing(mailing_id):
    mailing = Mailing.objects.get(id=mailing_id)
    current_datetime = datetime.now(timezone.utc)

    # Обновляем статус рассылки на 'started'
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


# from datetime import datetime, timezone
#
# from config.celery import app
# from django.core.mail import send_mail, BadHeaderError
#
# from config.settings import EMAIL_HOST_USER
# from mailing.models import Mailing, MailingLog
#
#
# @app.task()
# def start_mailing():
#     # Получаем все объекты Mailing из базы данных
#     mailings = Mailing.objects.all()
#
#     # Перебираем каждый объект Mailing
#     for mailing in mailings:
#         # Проверяем статус рассылки
#         if mailing.status not in ['created', 'started']:
#             # Если статус не является 'created' или 'started', переходим к следующему объекту
#             continue
#
#         # Получаем текущее время и дату
#         current_datetime = datetime.now(timezone.utc)
#
#         # Проверяем, наступила ли дата начала рассылки
#         if current_datetime.date() >= mailing.start_date:
#             # Проверяем, не наступила ли дата окончания рассылки
#             if current_datetime.date() <= mailing.end_date:
#                 # Проверяем, наступило ли время начала рассылки
#                 if mailing.start_time is None or current_datetime.time() >= mailing.start_time:
#                     # Если все условия выполнены, обновляем статус рассылки на 'started'
#                     mailing.status = 'started'
#                     mailing.save()
#
#                     for client in mailing.clients.all():
#                         try:
#                             message_subject = mailing.get_message_subject()
#                             message_body = mailing.get_message_body()
#                             send_mail(
#                                 subject=message_subject,
#                                 message=message_body,
#                                 from_email=EMAIL_HOST_USER,
#                                 recipient_list=[client.client_email],
#                             )
#                             # Создаем запись в логах рассылки при успешной отправке
#                             MailingLog.objects.create(
#                                 message=mailing.message_set.first(),
#                                 attempt_time=current_datetime,
#                                 status='success',
#                                 server_response='Mail sent successfully',
#                             )
#                         except BadHeaderError as e:
#                             # Создаем запись в логах рассылки при ошибке отправки
#                             MailingLog.objects.create(
#                                 message=mailing.message_set.first(),
#                                 attempt_time=current_datetime,
#                                 status='error',
#                                 server_response=str(e),
#                             )
#                         except Exception as e:
#                             # Обработка других ошибок при отправке сообщения
#                             # создаем запись в логах рассылки
#                             MailingLog.objects.create(
#                                 message=mailing.message_set.first(),
#                                 attempt_time=current_datetime,
#                                 status='error',
#                                 server_response=str(e),
#                             )
