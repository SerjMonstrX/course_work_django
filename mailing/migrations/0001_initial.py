# Generated by Django 4.2.10 on 2024-03-10 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_email', models.EmailField(max_length=254, verbose_name='почта клиента')),
                ('full_name', models.CharField(max_length=200, verbose_name='ФИО')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='комментарий')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Клиент сервиса',
                'verbose_name_plural': 'Клиенты сервиса',
            },
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='название рассылки')),
                ('start_time', models.TimeField(blank=True, null=True, verbose_name='время рассылки')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='дата начала рассылки')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='дата завершения рассылки')),
                ('next_send', models.DateField(blank=True, null=True, verbose_name='дата следующей рассылки')),
                ('frequency', models.CharField(choices=[('daily', 'Ежедневно'), ('weekly', 'Еженедельно'), ('monthly', 'Ежемесячно')], max_length=20, verbose_name='периодичность')),
                ('status', models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена')], max_length=20, verbose_name='статус рассылки')),
                ('clients', models.ManyToManyField(blank=True, null=True, to='mailing.client', verbose_name='клиенты')),
            ],
            options={
                'verbose_name': 'Рассылка',
                'verbose_name_plural': 'Рассылки',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='тема письма')),
                ('body', models.TextField(verbose_name='тело письма')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Сообщение',
                'verbose_name_plural': 'Сообщения',
            },
        ),
        migrations.CreateModel(
            name='MailingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_time', models.DateTimeField(auto_now_add=True, verbose_name='дата и время последней попытки')),
                ('status', models.CharField(max_length=20, verbose_name='статус попытки')),
                ('server_response', models.TextField(blank=True, null=True, verbose_name='ответ сервера')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.client', verbose_name='клиент')),
                ('mailing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mailing.mailing', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'Логи рассылки',
                'verbose_name_plural': 'Логи рассылки',
            },
        ),
        migrations.AddField(
            model_name='mailing',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mailing.message', verbose_name='письмо для рассылки'),
        ),
        migrations.AddField(
            model_name='mailing',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='пользователь сервиса'),
        ),
    ]
