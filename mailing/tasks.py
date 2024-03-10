from datetime import datetime, timezone, timedelta
from config.celery import app
from django.core.mail import send_mail, BadHeaderError
from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, MailingLog
from django.db.models import Q


@app.task()
def start_mailing():
    mailings = Mailing.objects.filter(Q(status='created') | Q(status='started'))
    current_datetime = datetime.now(timezone.utc)

    for mailing in mailings:
        # Если дата начала рассылки еще не наступила, пропускаем эту рассылку
        if current_datetime.date() < mailing.start_date:
            continue

        # Если дата окончания рассылки уже наступила, то меняем статус и завершаем рассылку.
        if current_datetime.date() > mailing.end_date:
            mailing.status = 'completed'
            mailing.save()
            continue

        # Проверяем наступила ли дата следующей отправки
        if mailing.next_send < current_datetime.date() and mailing.start_time < current_datetime.time():
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
                        mailing=mailing.title,
                        client=client.client_email,
                        attempt_time=current_datetime,
                        status='success 200',
                        server_response='Сообщение успешно отправлено',
                    )

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
                        mailing=mailing.title,
                        client=client.client_email,
                        attempt_time=current_datetime,
                        status='error 500',
                        server_response=str(e),
                    )

                except ValueError as e:
                    # Обработка ошибок ValueError
                    # создаем запись в логах рассылки
                    MailingLog.objects.create(
                        mailing=mailing.title,
                        client=client.client_email,
                        attempt_time=current_datetime,
                        status='error 400',
                        server_response=str(e),
                    )

                except Exception as e:
                    # Обработка других ошибок при отправке сообщения
                    # создаем запись в логах рассылки
                    MailingLog.objects.create(
                        mailing=mailing.title,
                        client=client.client_email,
                        attempt_time=current_datetime,
                        status='error',
                        server_response=str(e),
                    )
